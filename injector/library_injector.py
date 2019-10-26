# -*- coding: utf-8 -*-
import sys
from injector.args.parser import parse_args


def main():
    argv = sys.argv[1:]
    parsed_object = parse_args(argv)


if __name__ == '__main__':
    main()
