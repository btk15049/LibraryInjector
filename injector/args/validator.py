# -*- coding: utf-8 -*-
import argparse


class ArgumentCombinationError(Exception):
    pass


def validate_if_see_only(args: argparse.Namespace):
    if args.action == 'see-dependency' and args.inplace:
        raise ArgumentCombinationError(
            "If a '--action' value is 'see-dependency', '--inplace' flag should not be set.")


def validate_args(args: argparse.Namespace):
    validate_if_see_only(args)
