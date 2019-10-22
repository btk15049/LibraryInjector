# -*- coding: utf-8 -*-
from injector.args.parser import parse_args
import unittest


class ArgumentParserTest(unittest.TestCase):
    def test_file(self):
        parsed_object = parse_args(['main.cpp'])
        self.assertEqual(parsed_object.file, 'main.cpp')

    def test_action_param(self):
        parsed_object = parse_args(['main.cpp'])
        self.assertEqual(parsed_object.file, 'main.cpp')
        self.assertEqual(parsed_object.action, 'inject-library')

        parsed_object = parse_args(
            ['main.cpp', '--action', 'inject-library'])
        self.assertEqual(parsed_object.file, 'main.cpp')
        self.assertEqual(parsed_object.action, 'inject-library')

        parsed_object = parse_args(
            ['main.cpp', '--action', 'see-dependency'])
        self.assertEqual(parsed_object.file, 'main.cpp')
        self.assertEqual(parsed_object.action, 'see-dependency')

    def test_inplace_flag(self):
        parsed_object = parse_args(['main.cpp'])
        self.assertEqual(parsed_object.file, 'main.cpp')
        self.assertEqual(parsed_object.inplace, False)

        parsed_object = parse_args(['main.cpp', '--inplace'])
        self.assertEqual(parsed_object.file, 'main.cpp')
        self.assertEqual(parsed_object.inplace, True)

    def test_no_stdout_flag(self):
        parsed_object = parse_args(['main.cpp'])
        self.assertEqual(parsed_object.file, 'main.cpp')
        self.assertEqual(parsed_object.no_stdout, False)

        parsed_object = parse_args(
            ['main.cpp', '--no-stdout'])
        self.assertEqual(parsed_object.file, 'main.cpp')
        self.assertEqual(parsed_object.no_stdout, True)

    def test_mixed_file_and_multi_options(self):
        parsed_object = parse_args(
            ['--inplace', 'main.cpp', '--no-stdout'])
        self.assertEqual(parsed_object.file, 'main.cpp')
        self.assertEqual(parsed_object.no_stdout, True)
        self.assertEqual(parsed_object.inplace, True)


if __name__ == '__main__':
    unittest.main()
