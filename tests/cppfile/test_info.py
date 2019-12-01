# -*- coding: utf-8 -*-
from injector.cppfile.info import *
import unittest
import tempfile
import os
from unittest.mock import patch, call, MagicMock


class InfoTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = tempfile.TemporaryDirectory()

    def tearDown(self) -> None:
        self.root.cleanup()

    def setUpFiles(self, files: [str]) -> None:
        for f_name in files:
            p = pathlib.Path(self.root.name + os.sep + f_name)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.touch(exist_ok=True)

    def test_include(self):
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
            'local': {
                0: pathlib.Path(self.root.name + os.sep + 'lib1/a.hpp'),
                1: pathlib.Path(self.root.name + os.sep + 'lib1/b.hpp'),
                2: pathlib.Path(self.root.name + os.sep + 'lib1/A/a.hpp'),
                3: pathlib.Path(self.root.name + os.sep + 'lib1/A/b.hpp'),
                4: pathlib.Path(self.root.name + os.sep + 'lib1/B/a.hpp'),
                5: pathlib.Path(self.root.name + os.sep + 'lib2/c.hpp'),
                6: pathlib.Path(self.root.name + os.sep + 'lib2/A/d.hpp'),
            },
            'stl': {
                7: 'iostream',
            },
        }
        self.setUpFiles(files)
        actual = Include(
            source=args['source'],
            lib_dirs=args['lib_dirs'])
        self.assertEqual(expected['local'], actual.local)
        self.assertEqual(expected['stl'], actual.stl)

    def test_implement(self):
        source = [
            'a',
            'bb',
            'ccc',
            '   dd',
        ]
        impl = Implement(source)
        expected = {
            0: 'a',
            1: 'bb',
            2: 'ccc',
            3: '   dd',
        }
        self.assertEqual(expected, impl.implement)
        expected = {
            1: 'bb',
            2: 'ccc',
            3: '   dd',
        }
        impl = Implement(source, [0])
        self.assertEqual(expected, impl.implement)
        expected = {
            1: 'bb',
            3: '   dd',
        }
        impl = Implement(source, [0], [0, 2])
        self.assertEqual(expected, impl.implement)

    def test_source(self):
        files = [
            'a.cpp',
        ]
        self.setUpFiles(files)

        with patch('injector.cppfile.info.Include', MagicMock(return_value=MagicMock(stl={}, local={}))) as include:
            with patch('injector.cppfile.info.Source.load', MagicMock(return_value=None)) as load:
                with patch('injector.cppfile.info.Implement', MagicMock(return_value=MagicMock())) as implement:
                    cpp = self.root.name + os.sep + 'a.cpp'
                    hpp = self.root.name + os.sep + 'a.hpp'
                    actual = Source(cpp)

                    # check include
                    self.assertEqual(1, include.call_count)
                    self.assertIsNone(actual.hpp)
                    self.assertIsNone(actual.cpp)

                    # check load
                    calls = [
                        call(hpp),
                        call(cpp),
                    ]
                    expected_hpps_set = set()
                    expected_cpps_set = set()
                    self.assertEqual(2, load.call_count)
                    self.assertEqual(expected_hpps_set, Source.hpps)
                    self.assertEqual(expected_cpps_set, Source.cpps)
                    load.assert_has_calls(calls, any_order=True)

                    # check implement
                    self.assertEqual(1, implement.call_count)

        with patch('injector.cppfile.info.Include', MagicMock(return_value=MagicMock(stl={}, local={}))) as include:
            with patch('injector.cppfile.info.Source.load', MagicMock(return_value='mock')) as load:
                with patch('injector.cppfile.info.Implement', MagicMock(return_value=MagicMock())) as implement:
                    cpp = self.root.name + os.sep + 'a.cpp'
                    hpp = self.root.name + os.sep + 'a.hpp'
                    actual = Source(cpp)

                    # check include
                    self.assertEqual(1, include.call_count)
                    self.assertEqual('mock', actual.hpp)
                    self.assertEqual('mock', actual.cpp)

                    # check load
                    calls = [
                        call(hpp),
                        call(cpp),
                    ]
                    self.assertEqual(2, load.call_count)
                    expected_hpps_set = set()
                    expected_cpps_set = set()
                    expected_hpps_set.add(hpp)
                    expected_cpps_set.add(cpp)
                    self.assertEqual(expected_hpps_set, Source.hpps)
                    self.assertEqual(expected_cpps_set, Source.cpps)
                    load.assert_has_calls(calls, any_order=True)

                    # check implement
                    self.assertEqual(1, implement.call_count)

    def test_source_load(self):
        self.setUpFiles(['mock/cache', 'mock/mock'])
        Source.cache[self.root.name + os.sep + 'mock/cache'] = 'cache'
        Source.cache['none'] = None
        # file is not found
        with patch('injector.cppfile.info.Source.__init__', MagicMock(return_value=None)) as source:
            actual = Source.load('none')
            self.assertIsNone(actual)
            self.assertEqual(0, source.call_count)
        # use cache
        with patch('injector.cppfile.info.Source.__init__', MagicMock(return_value=None)) as source:
            actual = Source.load(self.root.name + os.sep + 'mock/cache')
            self.assertEqual('cache', actual)
            self.assertEqual(0, source.call_count)
        # use constructor
        with patch('injector.cppfile.info.Source.__init__', MagicMock(return_value=None)) as source:
            actual = Source.load(self.root.name + os.sep + 'mock/mock')
            self.assertIsNotNone(actual)
            self.assertEqual(source.call_count, 1)
