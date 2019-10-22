# -*- coding: utf-8 -*-
import sys
from injector.args.parser import parse_args

if __name__ == '__main__':
    argv = sys.argv[1:]
    parsed_object = parse_args(argv)
