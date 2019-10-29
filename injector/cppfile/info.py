# -*- coding: utf-8 -*-
import pathlib
import re
import os


class Include:
    local_matcher = re.compile(r'[\s]*#[\s]*include[\s]*\"([^\"]+)\"')
    stl_matcher = re.compile(r'[\s]*#[\s]*include[\s]*\<([^\>]+)\>')

    def __init__(self, source: [str], lib_dirs: [str]) -> None:
        headers = list(map(lambda h: h.group(1), filter(
            lambda h: h is not None, map(
                Include.local_matcher.search, source))))
        self.local = []
        for header in headers:
            for lib_dir in lib_dirs:
                if pathlib.Path(lib_dir + os.sep + header).exists():
                    self.local.append(lib_dir + os.sep + header)
        self.stl = list(map(lambda h: h.group(1), filter(
            lambda h: h is not None, map(
                Include.stl_matcher.search, source))))


class Source:
    cache = {}

    def __init__(self, path: str) -> None:
        self.path = pathlib.Path(path)
        self.cpp = Source.load(self.path.stem + '.cpp')
        self.hpp = Source.load(self.path.stem + '.hpp')
        self.includes = Include(self.path.read_text().splitlines())

    @staticmethod
    def load(path: str):
        if path not in Source.cache:
            Source.cache[path] = Source(path)
        return Source.cache[path]


class Info:
    def __init__(self, path) -> None:
        pass
