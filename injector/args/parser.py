# -*- coding: utf-8 -*-
import argparse


def parse_args(args: [str]):
    parser = argparse.ArgumentParser(
        description='This command line tool is prepared for competitive programing. \n'
                    'First, it extracts dependencies between C/C++ source code in your library. \n'
                    'Finally, it inject your library into a code, and make it runnable at online judge.')
    parser.add_argument(
        'file',
        help='Main C/C++ source code')
    parser.add_argument(
        '--action',
        choices=[
            'inject-library',
            'see-dependency'],
        default='inject-library')
    parser.add_argument(
        '-L',
        '--library',
        help='A directory path of your library. Note that you should be full path.')
    parser.add_argument(
        '-i',
        '--inplace',
        action='store_true',
        help='When you set this option, injector overwrite your main file. This option work when only --action is '
             '\'inject-library\'.')
    parser.add_argument(
        '--no-stdout',
        action='store_true')
    parser.add_argument(
        '--output-file')
    parser.add_argument(
        '--no-color',
        action='store_true')
    return parser.parse_args(args)
