# -*- coding: utf-8 -*-
import sys
from injector.args.parser import parse_args
from injector.args.validator import validate_args


def main():
    argv = sys.argv[1:]
    parsed_args = parse_args(argv)
    del argv
    validate_args(parsed_args)


if __name__ == '__main__':
    main()
