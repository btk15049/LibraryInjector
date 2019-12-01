# -*- coding: utf-8 -*-
import pathlib
import re
import os
import logging


class Include:
    local_matcher = re.compile(r'[\s]*#[\s]*include[\s]*\"([^\"]+)\"')
    stl_matcher = re.compile(r'[\s]*#[\s]*include[\s]*\<([^\>]+)\>')

    def __init__(self, source: [str], lib_dirs: [str]):
        self.local: {int, str} = {}
        self.stl: {int, str} = {}
        for si in range(len(source)):
            # find local header
            match_result = Include.local_matcher.search(source[si])
            if match_result is not None:
                header = match_result.group(1)
                for lib_dir in lib_dirs:
                    path = pathlib.Path(lib_dir + os.sep + header)
                    if path.exists():
                        self.local[si] = path
            # get stl
            match_result = Include.stl_matcher.search(source[si])
            if match_result is not None:
                header = match_result.group(1)
                self.stl[si] = header


class Implement:
    def __init__(self, source: [str], *args):
        self.implement: {int, str} = {}
        excludes = set()
        for arg in args:
            for i in arg:
                excludes.add(i)
        for si in range(len(source)):
            if si not in excludes:
                self.implement[si] = source[si]


class Source:
    cache = {}
    hpps = set()
    cpps = set()

    def __init__(self, path: str):
        self.path = pathlib.Path(path)

        base = str(self.path.parent) + os.sep + self.path.stem

        hpp_name = base + '.hpp'
        self.hpp = Source.load(hpp_name)
        if self.hpp is not None:
            Source.hpps.add(hpp_name)

        cpp_name = base + '.cpp'
        self.cpp = Source.load(cpp_name)
        if self.cpp is not None:
            Source.cpps.add(cpp_name)

        self.content: [str] = self.path.read_text().splitlines()
        self.includes = Include(
            self.content,
            [])  # TODO: assign lib_dir

        self.implement = Implement(
            self.content, self.includes.stl.keys(), self.includes.local.keys())
        logging.info('{} is registered'.format(path))

    @staticmethod
    def load(path: str):
        if not pathlib.Path(path).exists():
            return None
        if path not in Source.cache:
            Source.cache[path] = Source(path)
        return Source.cache[path]


class Info:
    def __init__(self, path) -> None:
        pass
