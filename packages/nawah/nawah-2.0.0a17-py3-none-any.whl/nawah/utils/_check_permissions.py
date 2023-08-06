'''Provides 'check_permissions' Utility'''

import copy
import logging
from typing import TYPE_CHECKING, cast

from nawah.exceptions import NotPermittedException

if TYPE_CHECKING:
    from nawah.classes import Func, Module
    from nawah.types import NawahEnv

logger = logging.getLogger('nawah')


def check_permissions(*, func: 'Func', env: 'NawahEnv'):
    '''Matches Permission Sets against current session user privileges. Returns 'Func' object
    query_mod, doc_mod of Permission Set matched. If failed to match any, raises'''

    module = cast('Module', func.module)

    logger.debug(
        'Attempting to check permissions for \'%s\'.\'%s\' against \'%s\'',
        module.name,
        func.name,
        env['session']['user'],
    )

    # Loop over Permissions Set to find a match and return its query_mod, doc_mod
    for permission in func.permissions:
        # Check for allow-all *
        if permission.privilege == '*':
            return (
                copy.deepcopy(permission.query_mod),
                copy.deepcopy(permission.doc_mod),
            )
        # Set variables to use for checking permission
        privilege_module = module.name
        privilege = permission.privilege
        # If Permission Set privilege is dot-notated value, use it to set module, privilege
        if '.' in permission.privilege:
            privilege_module, privilege = permission.privilege.split('.')

        # Skip Permission Set if privilege_module not in user prvileges
        if privilege_module not in env['session']['user']['privileges']:
            continue

        if privilege not in env['session']['user']['privileges'][privilege_module]:
            continue

        return (copy.deepcopy(permission.query_mod), copy.deepcopy(permission.doc_mod))

    # If no match, raise NotPermittedException
    raise NotPermittedException(module_name=module.name, func_name=func.name)
