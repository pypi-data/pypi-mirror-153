import logging
import os
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import argparse

logger = logging.getLogger('nawah')

NAME_PATTERN = r'^[a-z][a-z0-9_]+$'


def create(args: 'argparse.Namespace'):
    '''Provides create command functionality to Nawah CLI'''

    if not re.match(r'^[a-z][a-z0-9_]+$', args.name):
        raise Exception(
            'Value for \'name\' CLI Arg is invalid. Name should have only small letters, '
            'numbers, and underscores.'
        )

    component = args.component
    path = os.path.realpath(args.path)

    logger.info(
        'Checking possibility to create component \'%s\', at \'%s\'', component, path
    )

    if os.path.exists(directory := os.path.join(path, args.name)):
        raise Exception(f'Path \'{path}\' already has item \'{args.name}\'')

    os.mkdir(directory)
    callables = {
        'app': create_app,
    }
    callables[component](directory, args.name, args.standalone)


def create_app(directory: str, name: str, _):
    with open(os.path.join(directory, '__init__.py'), 'w', encoding='UTF-8') as f:
        pass
