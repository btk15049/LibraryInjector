# -*- coding: utf-8 -*-
from injector.cppfile.info import *
import unittest
import tempfile
from typing import List, Dict


class ExtractIncludeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.root.cleanup()

    def sandbox_test(self, files: [str], args: [
                     str], expected: Dict[str, List[str]]):
        for f_name in files:
            p = pathlib.Path(self.root.name + os.sep + f_name)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch(exist_ok=True)
        actual = Include(
            args['source'],
            args['lib_dirs'])
        self.assertEqual(expected['local'], actual.local)
        self.assertEqual(expected['stl'], actual.stl)

    def test_extract_local_file(self):
        args = {
            'source': [
                '#include "a.hpp"',
                '#include "b.hpp"',
                '#include "A/a.hpp"',
                '#include "A/b.hpp"',
                '#include "B/a.hpp"',
                '#include "c.hpp"',
                '#include "A/d.hpp"',
                '#include <iostream>'],
            'lib_dirs': [
                self.root.name + os.sep + 'lib1',
                self.root.name + os.sep + 'lib2',
            ]
        }
        files = [
            'lib1/a.hpp',
            'lib1/b.hpp',
            'lib1/A/a.hpp',
            'lib1/A/b.hpp',
            'lib1/B/a.hpp',
            'lib2/c.hpp',
            'lib2/A/d.hpp',
        ]
        expected = {
            'local': [
                self.root.name + os.sep + 'lib1/a.hpp',
                self.root.name + os.sep + 'lib1/b.hpp',
                self.root.name + os.sep + 'lib1/A/a.hpp',
                self.root.name + os.sep + 'lib1/A/b.hpp',
                self.root.name + os.sep + 'lib1/B/a.hpp',
                self.root.name + os.sep + 'lib2/c.hpp',
                self.root.name + os.sep + 'lib2/A/d.hpp',
            ],
            'stl': [
                'iostream'
            ],
        }
        self.sandbox_test(files, args, expected)
