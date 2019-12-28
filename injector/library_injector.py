# -*- coding: utf-8 -*-
import sys
from termcolor import colored
from injector.args.parser import parse_args
from injector.args.validator import validate_args
from injector.cppfile.info import Info, Source


def wrap_region(code: [str], tag: str) -> [str]:
    return ['/* #region {} */'.format(tag), ''] + \
        code + ['', '/* #endregion {} */'.format(tag), '']


def build(info: Info) -> str:
    product: [str] = []
    for filename in info.compute_sorted():
        source = Source.load(filename)
        implement = list(source.implement.implement.values())
        product.extend(
            wrap_region(
                implement,
                source.path.stem))
    return '\n'.join(product)


def main():
    argv = sys.argv[1:]
    parsed_args = parse_args(argv)
    del argv
    validate_args(parsed_args)

    info = Info(parsed_args.file, parsed_args.library)
    submit_code = build(info)

    if parsed_args.no_stdout is False:
        if parsed_args.no_color is False:
            print(colored(submit_code, 'blue'))
        else:
            print(submit_code)


if __name__ == '__main__':
    main()
