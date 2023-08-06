'''Provides 'extract_val', 'set_val', 'expand_val' Utilities'''

import datetime
import logging
import os
import re
from typing import (TYPE_CHECKING, Any, Callable, MutableMapping,
                    MutableSequence, Union, cast)

from nawah.classes._jsonpath import JSONPath
from nawah.config import Config
from nawah.enums import VarType
from nawah.exceptions import (InvalidLocaleException, InvalidVarException,
                              JSONPathNotFoundException)

if TYPE_CHECKING:
    from nawah.classes import Var
    from nawah.types import NawahDoc, NawahEnv


logger = logging.getLogger('nawah')


def var_value(
    var: 'Var',
    /,
    *,
    env: 'NawahEnv' = None,
    doc: 'NawahDoc' = None,
    locale: str = None,
    return_type: Union[type | Callable[[Any], Any]] = None,
) -> Any:
    '''Retrieves current value of 'Var' object'''

    try:
        value = None
        match var.type:
            case VarType.ENV:
                var.var = cast(str, var.var)
                value = os.environ[var.var]

            case VarType.SESSION:
                var.var = cast(str, var.var)
                if not env:
                    raise Exception(
                        'Can\'t retrieve value for Var object of type \'SESSION\' with '
                        'no \'env\' arg provided'
                    )
                value = extract_val(scope=cast(Any, env['session']), path=var.var)

            case VarType.DOC:
                var.var = cast(str, var.var)
                if not doc:
                    raise Exception(
                        'Can\'t retrieve value for Var object of type \'DOC\' with '
                        'no \'doc\' arg provided'
                    )
                value = extract_val(scope=cast(Any, doc), path=var.var)

            case VarType.CONFIG:
                var.var = cast(str, var.var)
                value = extract_val(scope=Config.vars, path=var.var)

            case VarType.L10N:
                var.var = cast(str, var.var)
                if not locale:
                    raise Exception(
                        'Can\'t retrieve value for Var object of type \'L10N\' with '
                        'no \'locale\' arg provided'
                    )
                if locale not in Config.locales:
                    raise InvalidLocaleException(locale=locale)
                value = extract_val(scope=Config.l10n[locale], path=var.var)

            case VarType.DATE:
                return datetime.datetime.utcnow().isoformat().split('T')[0]

            case VarType.TIME:
                return datetime.datetime.utcnow().isoformat().split('T')[1]

            case VarType.DATETIME:
                return datetime.datetime.utcnow().isoformat()

            case _:
                raise Exception(f'Unknown Var Type \'{var.type}\'')

        if not return_type:
            return value

        return return_type(value)

    except (KeyError, ValueError) as e:
        raise InvalidVarException(var=var) from e


def _jsonpath_eval_func(*args):
    return eval(*args)


def extract_val(
    *, scope: MutableMapping[str, Any], path: str, return_array: bool = False
):
    '''Extracts value from provided 'scope' with JSONPath-based 'path' '''

    if path.startswith('$__'):
        path = path[3:]

    attr = JSONPath(path).parse(scope, eval_func=_jsonpath_eval_func)

    if return_array:
        return attr

    if len(attr) == 0:
        raise JSONPathNotFoundException(scope=scope, attr_path=path)

    return attr[0]


def set_val(*, scope: dict[str, Any], path: str, value: Any):
    '''Sets value to object from provided 'scope' with JSONPath-based 'path' '''

    if path.startswith('$__'):
        path = path[3:]

    # Find the path to target parent
    attr_path_parent = '.'.join(path.split('.')[:-1])

    # Set 'attr' to list containing 'scope', to have value for attr
    # if 'attr_path_parent' is empty, skipping JSONPath parse
    attr = [scope]

    if attr_path_parent:
        attr = JSONPath(attr_path_parent).parse(scope, eval_func=_jsonpath_eval_func)

    if len(attr) == 0:
        raise JSONPathNotFoundException(scope=scope, attr_path=path)

    attr_path_last: Union[str, int] = path.split('.')[-1]
    if re.match(r'^[0-9]$', cast(str, attr_path_last)):
        attr_path_last = int(attr_path_last)

    for child_attr in attr:
        child_attr[
            attr_path_last if isinstance(child_attr, list) else str(attr_path_last)
        ] = value


def expand_val(
    *, doc: MutableMapping[str, Any], expanded_doc: MutableMapping[str, Any] = None
):
    '''Expands dot-notated keys in dict to its full path'''

    if not expanded_doc:
        expanded_doc = {}
    for attr in doc:
        if isinstance(doc[attr], dict):
            doc[attr] = expand_val(doc=doc[attr])
        if '.' in attr:
            attr_path = attr.split('.')
            scope = expanded_doc
            for i in range(len(attr_path) - 1):
                try:
                    if not isinstance(scope[attr_path[i]], dict):
                        scope[attr_path[i]] = {}
                except KeyError:
                    scope[attr_path[i]] = {}
                scope = scope[attr_path[i]]
            scope[attr_path[-1]] = doc[attr]
        else:
            expanded_doc[attr] = doc[attr]
    return expanded_doc


def deep_update(
    *,
    target: Union[MutableMapping, MutableSequence],
    new_values: Union[MutableMapping, MutableSequence],
):
    '''Updates values from two dics, lists recursively down to the last child'''

    if not isinstance(target, type(new_values)):
        # [TODO] Refactor as custom exception
        raise Exception(
            f'Type \'{type(target)}\' of \'target\' is not the same as \'{type(new_values)}\''
            'of \'new_values\'',
        )

    if isinstance(new_values, dict):
        new_values = cast(dict, new_values)
        for k in new_values.keys():
            target = cast(dict, target)
            if k not in target.keys():
                target[k] = new_values[k]
            else:
                deep_update(target=target[k], new_values=new_values[k])
    elif isinstance(new_values, list):
        for j in new_values:
            target = cast(list, target)
            if j not in target:
                target.append(j)

def camel_to_upper(val: str, /) -> str:
    '''Converts 'val' from CamelCase to UPPER_CASE'''

    # [REF] https://stackoverflow.com/a/1176023
    return re.sub(r'(?<!^)(?=[A-Z])', '_', val).upper()
