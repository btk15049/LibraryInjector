# -*- coding: utf-8 -*-
import pathlib
import re
import os
import logging
from injector.algorithm.topological_sort import topological_sort


class Include:
    local_matcher = re.compile(r'[\s]*#[\s]*include[\s]*\"([^\"]+)\"')
    stl_matcher = re.compile(r'[\s]*#[\s]*include[\s]*\<([^\>]+)\>')

    def __init__(self, source: [str], *lib_dirs):
        self.local: {int, str} = {}
        self.stl: {int, str} = {}
        for si in range(len(source)):
            # find local header
            match_result = Include.local_matcher.search(source[si])
            if match_result is not None:
                header = match_result.group(1)
                for lib_dir in lib_dirs:
                    path = pathlib.Path(lib_dir) / header
                    if path.exists():
                        self.local[si] = str(path)
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

    def __init__(self, path: str, *lib_dirs):
        self.path = pathlib.Path(path)

        base = str(self.path.parent) + os.sep + self.path.stem

        hpp_name = base + '.hpp'
        if path == hpp_name:
            self.hpp = self
        else:
            self.hpp = Source.load(hpp_name, *lib_dirs)
        if self.hpp is not None:
            Source.hpps.add(hpp_name)

        cpp_name = base + '.cpp'
        if path == cpp_name:
            self.cpp = self
        else:
            self.cpp = Source.load(cpp_name, *lib_dirs)
        if self.cpp is not None:
            Source.cpps.add(cpp_name)

        self.content: [str] = self.path.read_text().splitlines()
        self.includes = Include(
            self.content, *lib_dirs)
        for v in self.includes.local.values():
            self.load(v, *lib_dirs)
        self.implement = Implement(
            self.content, self.includes.stl.keys(), self.includes.local.keys())
        logging.info('{} is registered'.format(path))

    @staticmethod
    def load(path: str, *lib_dirs):
        if not pathlib.Path(path).exists():
            return None
        if path not in Source.cache:
            Source.cache[path] = None
            source = Source(path, *lib_dirs)
            Source.cache[path] = source
        return Source.cache[path]

    @staticmethod
    def clear_cache():
        Source.hpps = set()
        Source.cpps = set()


class Info:
    def __init__(self, path: str, *lib_dirs) -> None:
        self.root: str = path
        self.sources: [str] = []
        self.lib_dirs = lib_dirs
        Source.clear_cache()
        # Sourceクラスのキャッシュに関連ファイルを読ませておく
        Source.load(path, *self.lib_dirs)
        self.sources.extend(list(Source.hpps))
        self.sources.extend(list(Source.cpps))

    def compute_sorted(self) -> [Source]:
        edges = {
            source: Source.load(
                source,
                self.lib_dirs).includes.local.values() for source in self.sources}
        logging.info('nodes: ' + str(self.sources))
        logging.info('edges: ' + str(edges))
        return topological_sort(self.sources, edges)
