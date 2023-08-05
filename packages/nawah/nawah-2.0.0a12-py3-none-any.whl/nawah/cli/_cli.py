'''Provides function to create CLI for Nawah'''

import argparse

from nawah import __version__

from ._create import create


def cli():
    '''Creates CLI for Nawah'''

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--version',
        help='Print Nawah version and exit',
        action='version',
        version=f'Nawah v{__version__}',
    )

    subparsers = parser.add_subparsers(
        title='Command',
        description='Nawah CLI command to run',
        dest='command',
    )

    parser_create = subparsers.add_parser('create', help='Create new Nawah app')
    parser_create.set_defaults(func=create)
    parser_create.add_argument(
        'component',
        help='Type of component to create',
        choices=['app', 'package', 'module'],
    )

    parser_create.add_argument(
        'name',
        type=str,
        help='Name of component to create',
    )

    parser_create.add_argument(
        'path',
        type=str,
        nargs='?',
        help='Path to create component in [default .]',
        default='.',
    )

    parser_create.add_argument(
        '--standalone',
        help='When creating Nawah package, add this flag to create standalone Python project '
        'for Nawah package. This allows developing Nawah package in isolation, with ability to '
        'publish it as Python package and use it across multiple apps. If you are intending to '
        'use the package in one app only, don\'t use this flag, and point path to Nawah app '
        'folder, to only create project sub-package',
        action='store_true',
    )

    args = parser.parse_args()

    if args.command:
        args.func(args)

    else:
        parser.print_help()
