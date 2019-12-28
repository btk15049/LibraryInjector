# -*- coding: utf-8 -*-
import sys
import pathlib
from termcolor import colored
from injector.args.parser import parse_args
from injector.args.validator import validate_args
from injector.cppfile.info import Info, Source


def wrap_region(code: [str], tag: str) -> [str]:
    return ['/* #region {} */'.format(tag), ''] + \
        code + ['', '/* #endregion {} */'.format(tag), '']


def build(info: Info) -> str:
    stl: [str] = []
    product: [str] = []
    for filename in info.compute_sorted():
        source = Source.load(filename)
        implement = list(source.implement.implement.values())
        product.extend(
            wrap_region(
                implement,
                source.path.stem))
        stl.extend(source.includes.stl.values())
    stl = wrap_region(['#include <{}>'.format(lib)
                       for lib in sorted(set(stl))], 'stl')
    return '\n'.join(stl + product)


def output(
        text: str,
        stdout_flag: bool,
        colored_flag: bool,
        output_file) -> None:
    if stdout_flag is True:
        if colored_flag is True:
            print(colored(text, 'blue'))
        else:
            print(text)
    if output_file is not None:
        pathlib.Path(output_file).write_text(text)


def main():
    argv = sys.argv[1:]
    parsed_args = parse_args(argv)
    del argv
    validate_args(parsed_args)

    info = Info(parsed_args.file, parsed_args.library)

    if parsed_args.action == 'inject-library':
        submit_code = build(info)
        output(
            submit_code,
            parsed_args.no_stdout is False,
            parsed_args.no_color is False, parsed_args.output_file)


if __name__ == '__main__':
    main()
