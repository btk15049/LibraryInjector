# -*- coding: utf-8 -*-
from injector.args.validator import *
import unittest
from unittest.mock import MagicMock, patch


class ArgumentValidatorTest(unittest.TestCase):
    def test_validate_if_see_only(self):
        validate_if_see_only(
            argparse.Namespace(
                action='see-dependency',
                inplace=False))
        validate_if_see_only(
            argparse.Namespace(
                action='otherwise',
                inplace=True))
        with self.assertRaises(ArgumentCombinationError):
            validate_if_see_only(
                argparse.Namespace(
                    action='see-dependency',
                    inplace=True))

    def test_validate_args(self):
        with patch('injector.args.validator.validate_if_see_only') as mock:
            validate_args(argparse.Namespace)
            self.assertEqual(mock.call_count, 1)

        with patch('injector.args.validator.validate_if_see_only', side_effect=ArgumentCombinationError) as mock:
            with self.assertRaises(ArgumentCombinationError):
                validate_args(argparse.Namespace())
            self.assertEqual(mock.call_count, 1)
