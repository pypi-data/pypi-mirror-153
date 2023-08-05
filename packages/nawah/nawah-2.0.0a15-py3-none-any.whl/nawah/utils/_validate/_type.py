'''Provides 'validate_type' Utility'''

import inspect
import logging
import re
from typing import TYPE_CHECKING, Any

from nawah.classes import Attr
from nawah.config import Config
from nawah.enums import AttrType
from nawah.exceptions import (InvalidAttrTypeArgException,
                              InvalidAttrTypeException,
                              InvalidAttrTypeRefException)

from .._shared import ATTRS_TYPES_ARGS

if TYPE_CHECKING:

    from .._shared import AttrTypeArgValidation

logger = logging.getLogger('nawah')


ATTR_TYPE_ARG_TYPE_MAP = {
    'Attr': lambda arg_val: isinstance(arg_val, Attr),
    'bool': lambda arg_val: isinstance(arg_val, bool),
    'callable': lambda arg_val: callable(arg_val)
    or inspect.iscoroutinefunction(arg_val),
    'dict': lambda arg_val: isinstance(arg_val, dict),
    'float': lambda arg_val: isinstance(arg_val, float),
    'int': lambda arg_val: isinstance(arg_val, int),
    'list': lambda arg_val: isinstance(arg_val, list),
    'str': lambda arg_val: isinstance(arg_val, str),
    'union': lambda arg_val: isinstance(arg_val, list),
}


def validate_type(attr_type: 'Attr', skip_type: bool = False):
    '''Validates Attr Type objects. If failed, raises 'InvalidAttrTypeException' '''
    # Skip validating Attr Type if it is already validated
    if skip_type and attr_type.valid:
        return

    if attr_type.type not in AttrType:
        raise InvalidAttrTypeException(attr_type=attr_type)

    if attr_type.type == AttrType.TYPE:
        if skip_type:
            Config.sys.type_attrs.append(attr_type)
            return

        if isinstance(attr_type.args['type'], str):
            if attr_type.args['type'] not in Config.types:
                raise InvalidAttrTypeRefException(attr_type=attr_type)
            if not callable(Config.types[attr_type.args['type']]):
                raise InvalidAttrTypeRefException(attr_type=attr_type)
            # Assign new Attr Type Arg for shorthand calling the TYPE function
            attr_type.args['func'] = Config.types[attr_type.args['type']]
        else:
            if not inspect.iscoroutinefunction(attr_type.args['type']):
                raise InvalidAttrTypeRefException(attr_type=attr_type)
            # Assign new Attr Type Arg for shorthand calling the TYPE function
            attr_type.args['func'] = attr_type.args['type']

        attr_type.valid = True
        return

    for arg in (attr_type_args := ATTRS_TYPES_ARGS[attr_type.type.name]):
        try:
            if 'required' in attr_type_args[arg] or arg in attr_type.args:
                _validate_type_arg(
                    arg_name=arg,
                    arg_type=attr_type_args[arg],
                    arg_val=attr_type.args[arg],
                    skip_type=skip_type,
                )
        except InvalidAttrTypeArgException as e:
            raise InvalidAttrTypeException(attr_type=attr_type) from e

    attr_type.valid = True


def _validate_type_arg(
    arg_name: str, arg_type: 'AttrTypeArgValidation', arg_val: Any, skip_type: bool
):
    '''Validates Attr Type objects args. If failed, raises 'InvalidAttrTypeArgException' '''

    if not ATTR_TYPE_ARG_TYPE_MAP[arg_type['type']](arg_val):
        if 'required' in arg_type:
            raise InvalidAttrTypeArgException(
                arg_name=arg_name, arg_type=arg_type, arg_val=arg_val
            )

    if arg_val is None:
        return

    if arg_type['type'] == 'dict':
        for key, val in arg_val.items():
            _validate_type_arg(
                arg_name=f'{arg_name}.{key}',
                arg_type=arg_type['dict_key_type'],
                arg_val=key,
                skip_type=skip_type,
            )
            _validate_type_arg(
                arg_name=f'{arg_name}.{key}.val',
                arg_type=arg_type['dict_val_type'],
                arg_val=val,
                skip_type=skip_type,
            )
        return

    if arg_type['type'] == 'list':
        if arg_type['list_len_range'] is not None:
            if not (
                arg_type['list_len_range'][0]
                <= len(arg_val)
                < arg_type['list_len_range'][1]
            ):
                raise InvalidAttrTypeArgException(
                    arg_name=arg_name, arg_type=arg_type, arg_val=arg_val
                )
        for i, _ in enumerate(arg_val):
            _validate_type_arg(
                arg_name=f'{arg_name}.{i}',
                arg_type=arg_type['list_item_type'],
                arg_val=arg_val[i],
                skip_type=skip_type,
            )
        return

    if arg_type['type'] == 'str':
        if 'str_pattern' in arg_type:
            if not re.match(f'^{arg_type["str_pattern"]}$', arg_val):
                raise InvalidAttrTypeArgException(
                    arg_name=arg_name, arg_type=arg_type, arg_val=arg_val
                )
        return

    if arg_type['type'] == 'float':
        if isinstance(arg_val, (int, float)):
            return

    if arg_type['type'] == 'union':
        for union_type in arg_type['union_types']:
            # For union arg type, loop over all allowed types, validate
            # arg_val against all of them, and break when one successes,
            # Otherwise raise InvalidAttrTypeArgException
            try:
                _validate_type_arg(
                    arg_name=arg_name,
                    arg_type=union_type,
                    arg_val=arg_val,
                    skip_type=skip_type,
                )
                return
            except InvalidAttrTypeArgException:
                pass

    if arg_type['type'] == 'Attr':
        validate_type(attr_type=arg_val, skip_type=skip_type)
        return

    raise InvalidAttrTypeArgException(
        arg_name=arg_name, arg_type=arg_type, arg_val=arg_val
    )
