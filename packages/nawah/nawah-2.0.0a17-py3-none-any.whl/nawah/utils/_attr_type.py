'''Provides utilities related to Attr Type'''

import copy
import datetime
import logging
import math
import random
import re
from typing import Any, MutableMapping, MutableSequence, cast

from bson import ObjectId

from nawah.classes import Attr
from nawah.config import Config
from nawah.enums import AttrType, NawahValues
from nawah.exceptions import InvalidAttrTypeException

from ._shared import ATTRS_TYPES_ARGS
from ._validate import validate_type

logger = logging.getLogger('nawah')

def extract_attr(*, attrs: MutableMapping[str, 'Attr'], path: str) -> 'Attr':
    '''Extracts attr using its 'path' from 'attrs'. Attr path considers different Attr Types. For
    instance, to get child attr of Attr Type LIST, UNION, use index of child attr, to get 'key',
    'val' attrs of Attr Type KV_DICT use the arg name, to get child attr of Attr Type TYPED_DICT
    use key from 'dict' arg'''

    scope: MutableMapping[str, 'Attr'] | MutableSequence['Attr'] = attrs
    path_part: int | str
    path_parts = path.split('.')
    _iter = enumerate(path_parts)
    for _, path_part in _iter:
        if re.match('^[0-9]+$', cast(str, path_part)):
            path_part = int(path_part)
            path_part_check = path_part in range(len(scope))
        else:
            path_part_check = path_part in scope

        if not path_part_check:
            raise ValueError(
                f'Attr \'{path_part}\' does not exist in scope \'{scope}\''
            )

        scope_attr = cast(MutableMapping[str, 'Attr'], scope)[cast(str, path_part)]

        while scope_attr.type in [AttrType.LIST, AttrType.UNION]:
            try:
                _, path_part = next(_iter)
            except StopIteration:
                return scope_attr

            arg = 'list' if scope_attr.type == AttrType.LIST else 'union'
            scope_attr = scope_attr.args[arg][int(path_part)]

        while scope_attr.type == AttrType.KV_DICT:
            try:
                _, path_part = next(_iter)
            except StopIteration:
                return scope_attr

            scope_attr = scope_attr.args[path_part]

        while scope_attr.type == AttrType.TYPED_DICT:
            try:
                _, path_part = next(_iter)
            except StopIteration:
                return scope_attr

            scope_attr = scope_attr.args['dict'][path_part]


        match scope_attr.type:
            case AttrType.LIST:
                scope = scope_attr.args['list']
            case AttrType.UNION:
                scope = scope_attr.args['union']
            case AttrType.KV_DICT:
                scope = scope_attr.args['val']
            case AttrType.TYPED_DICT:
                scope = scope_attr.args['dict']

    return scope_attr

def encode_attr_type(*, attr_type: 'Attr') -> MutableMapping[str, Any]:
    '''Encodes Attr object into dict'''

    encoded_attr_type: MutableMapping[str, Any] = {
        'type': attr_type.type,
        'args': copy.deepcopy(attr_type.args),
        'allow_none': attr_type.default != NawahValues.NONE_VALUE,
        'default': attr_type.default
        if attr_type.default != NawahValues.NONE_VALUE
        else None,
    }
    # [DOC] Process args of type Attr
    if attr_type.type == AttrType.LIST:
        for i in range(len(attr_type.args['list'])):
            encoded_attr_type['args']['list'][i] = encode_attr_type(
                attr_type=attr_type.args['list'][i]
            )
    elif attr_type.type == AttrType.TYPED_DICT:
        for dict_attr in attr_type.args['dict'].keys():
            encoded_attr_type['args']['dict'][dict_attr] = encode_attr_type(
                attr_type=attr_type.args['dict'][dict_attr]
            )
    elif attr_type.type == AttrType.KV_DICT:
        encoded_attr_type['args']['key'] = encode_attr_type(
            attr_type=attr_type.args['key']
        )
        encoded_attr_type['args']['val'] = encode_attr_type(
            attr_type=attr_type.args['val']
        )
    elif attr_type.type == AttrType.UNION:
        for i in range(len(attr_type.args['union'])):
            encoded_attr_type['args']['union'][i] = encode_attr_type(
                attr_type=attr_type.args['union'][i]
            )
    elif attr_type.type == AttrType.TYPE:
        if callable(encoded_attr_type['args']['type']):
            raise Exception('Attr Type TYPE with callable \'type\' can\'t be encoded.')

        del encoded_attr_type['args']['func']

    return encoded_attr_type


def decode_attr_type(*, encoded_attr_type: MutableMapping[str, Any]) -> 'Attr':
    '''Converts Attr Type decoded into dict, back to Attr object'''
    # Fail-safe checks
    if encoded_attr_type['type'] not in ATTRS_TYPES_ARGS:
        raise InvalidAttrTypeException(attr_type=encoded_attr_type['type'])

    # Process args of type Attr
    if encoded_attr_type['type'] == 'LIST':
        for i, _ in enumerate(encoded_attr_type['args']['list']):
            encoded_attr_type['args']['list'][i] = decode_attr_type(
                encoded_attr_type=encoded_attr_type['args']['list'][i]
            )
    elif encoded_attr_type['type'] == 'TYPED_DICT':
        for dict_attr in encoded_attr_type['args']['dict'].keys():
            encoded_attr_type['args']['dict'][dict_attr] = decode_attr_type(
                encoded_attr_type=encoded_attr_type['args']['dict'][dict_attr]
            )
    elif encoded_attr_type['type'] == 'KV_DICT':
        encoded_attr_type['args']['key'] = decode_attr_type(
            encoded_attr_type=encoded_attr_type['args']['key']
        )
        encoded_attr_type['args']['val'] = decode_attr_type(
            encoded_attr_type=encoded_attr_type['args']['val']
        )
    if encoded_attr_type['type'] == 'UNION':
        for i in range(len(encoded_attr_type['args']['union'])):
            encoded_attr_type['args']['union'][i] = decode_attr_type(
                encoded_attr_type=encoded_attr_type['args']['union'][i]
            )
    # Generate dynamic Attr using Attr controller
    attr_type = getattr(Attr, encoded_attr_type['type'])(**encoded_attr_type['args'])

    # Validate Attr Type for possible Attr Type TYPE presence, to set Attr._args[func] value
    validate_type(attr_type=attr_type)

    return attr_type


def generate_attr_val(*, attr_type: Attr) -> Any:
    attr_val: Any

    if attr_type.type == AttrType.ANY:
        return '__any'

    if attr_type.type == AttrType.BOOL:
        attr_val = random.choice([True, False])
        return attr_val

    if attr_type.type == AttrType.DATE:
        if attr_type.args['ranges']:
            datetime_range = attr_type.args['ranges'][0]
            # [DOC] Be lazy! find a whether start, end of range is a datetime and base the value on it
            if datetime_range[0][0] in ['+', '-'] and datetime_range[1][0] in [
                '+',
                '-',
            ]:
                # [DOC] Both start, end are dynamic, process start
                datetime_range_delta = {}
                if datetime_range[0][-1] == 'd':
                    datetime_range_delta = {'days': int(datetime_range[0][:-1])}
                elif datetime_range[0][-1] == 'w':
                    datetime_range_delta = {'weeks': int(datetime_range[0][:-1])}
                attr_val = (
                    (
                        datetime.datetime.utcnow()
                        + datetime.timedelta(**datetime_range_delta)
                    )
                    .isoformat()
                    .split('T')[0]
                )
            else:
                if datetime_range[0][0] not in ['+', '-']:
                    attr_val = datetime_range[0]
                else:
                    attr_val = (
                        (
                            datetime.datetime.fromisoformat(datetime_range[1])
                            - datetime.timedelta(days=1)
                        )
                        .isoformat()
                        .split('T')[0]
                    )
        else:
            attr_val = datetime.datetime.utcnow().isoformat().split('T')[0]
        return attr_val

    if attr_type.type == AttrType.DATETIME:
        if attr_type.args['ranges']:
            datetime_range = attr_type.args['ranges'][0]
            # [DOC] Be lazy! find a whether start, end of range is a datetime and base the value on it
            if datetime_range[0][0] in ['+', '-'] and datetime_range[1][0] in [
                '+',
                '-',
            ]:
                # [DOC] Both start, end are dynamic, process start
                datetime_range_delta = {}
                if datetime_range[0][-1] == 'd':
                    datetime_range_delta = {'days': int(datetime_range[0][:-1])}
                elif datetime_range[0][-1] == 's':
                    datetime_range_delta = {'seconds': int(datetime_range[0][:-1])}
                elif datetime_range[0][-1] == 'm':
                    datetime_range_delta = {'minutes': int(datetime_range[0][:-1])}
                elif datetime_range[0][-1] == 'h':
                    datetime_range_delta = {'hours': int(datetime_range[0][:-1])}
                elif datetime_range[0][-1] == 'w':
                    datetime_range_delta = {'weeks': int(datetime_range[0][:-1])}
                attr_val = (
                    datetime.datetime.utcnow()
                    + datetime.timedelta(**datetime_range_delta)
                ).isoformat()
            else:
                if datetime_range[0][0] not in ['+', '-']:
                    attr_val = datetime_range[0]
                else:
                    attr_val = (
                        datetime.datetime.fromisoformat(datetime_range[1])
                        - datetime.timedelta(days=1)
                    ).isoformat()
        else:
            attr_val = datetime.datetime.utcnow().isoformat()
        return attr_val

    if attr_type.type == AttrType.KV_DICT:
        attr_val = {}
        if attr_type.args['req']:
            attr_val = {
                generate_attr_val(
                    attr_type=Attr.LITERAL(literal=[req])
                ): generate_attr_val(attr_type=attr_type.args['val'])
                for req in attr_type.args['req']
            }
        if attr_type.args['len_range']:
            for _ in range(attr_type.args['len_range'][0]):
                attr_val[
                    generate_attr_val(attr_type=attr_type.args['key'])
                ] = generate_attr_val(attr_type=attr_type.args['val'])
            return attr_val

        return attr_val

    if attr_type.type == AttrType.TYPED_DICT:
        attr_val = {
            child_attr: generate_attr_val(attr_type=attr_type.args['dict'][child_attr])
            for child_attr in attr_type.args['dict'].keys()
        }
        return attr_val

    if attr_type.type == AttrType.EMAIL:
        attr_val = f'some-{math.ceil(random.random() * 10000)}@mail.provider.com'
        if attr_type.args['allowed_domains']:
            if attr_type.args['strict_matching']:
                domain = 'mail.provider.com'
            else:
                domain = 'provider.com'
            attr_val = attr_val.replace(
                domain, random.choice(attr_type.args['allowed_domains'])
            )
        return attr_val

    if attr_type.type == AttrType.FILE:
        attr_file_type = 'text/plain'
        attr_file_extension = 'txt'
        if attr_type.args['types']:
            for file_type in attr_type.args['types']:
                if '/' in file_type:
                    attr_file_type = file_type
                if '*.' in file_type:
                    attr_file_extension = file_type.replace('*.', '')
        file_name = f'__file-{math.ceil(random.random() * 10000)}.{attr_file_extension}'
        return {
            'name': file_name,
            'lastModified': 100000,
            'type': attr_file_type,
            'size': 6,
            'content': b'__file',
        }

    if attr_type.type == AttrType.FLOAT:
        if attr_type.args['ranges']:
            attr_val = random.choice(
                range(
                    math.ceil(attr_type.args['ranges'][0][0]),
                    math.floor(attr_type.args['ranges'][0][1]),
                )
            )
            if (
                attr_val != attr_type.args['ranges'][0][0]
                and (attr_val - 0.01) != attr_type.args['ranges'][0][0]
            ):
                attr_val -= 0.01
            elif (attr_val + 0.01) < attr_type.args['ranges'][0][1]:
                attr_val += 0.01
            else:
                attr_val = float(attr_val)
        else:
            attr_val = random.random() * 10000
        return attr_val

    if attr_type.type == AttrType.GEO_POINT:
        return {
            'type': 'Point',
            'coordinates': [
                math.ceil(random.random() * 100000) / 1000,
                math.ceil(random.random() * 100000) / 1000,
            ],
        }

    if attr_type.type == AttrType.ID:
        return ObjectId()

    if attr_type.type == AttrType.INT:
        if attr_type.args['ranges']:
            attr_val = random.choice(
                range(attr_type.args['ranges'][0][0], attr_type.args['ranges'][0][1])
            )
        else:
            attr_val = math.ceil(random.random() * 10000)
        return attr_val

    if attr_type.type == AttrType.IP:
        return '127.0.0.1'

    if attr_type.type == AttrType.LIST:
        return [
            generate_attr_val(attr_type=random.choice(attr_type.args['list']))
            for _ in range(
                attr_type.args['len_range'][0] if attr_type.args['len_range'] else 0
            )
        ]

    if attr_type.type == AttrType.LOCALE:
        return {
            locale: f'__locale-{math.ceil(random.random() * 10000)}'
            for locale in Config.locales
        }

    if attr_type.type == AttrType.LOCALES:
        return Config.locale

    if attr_type.type == AttrType.PHONE:
        attr_phone_code = '000'
        if attr_type.args['codes']:
            attr_phone_code = random.choice(attr_type.args['codes'])
        return f'+{attr_phone_code}{math.ceil(random.random() * 10000)}'

    if attr_type.type == AttrType.STR:
        if attr_type.args['pattern']:
            logger.warning(
                'Generator for Attr Type STR can\'t handle patterns. Ignoring.'
            )
        return f'__str-{math.ceil(random.random() * 10000)}'

    if attr_type.type == AttrType.TIME:
        if attr_type.args['ranges']:
            datetime_range = attr_type.args['ranges'][0]
            # [DOC] Be lazy! find a whether start, end of range is a datetime and base the value on it
            if datetime_range[0][0] in ['+', '-'] and datetime_range[1][0] in [
                '+',
                '-',
            ]:
                # [DOC] Both start, end are dynamic, process start
                datetime_range_delta = {}
                if datetime_range[0][-1] == 's':
                    datetime_range_delta = {'seconds': int(datetime_range[0][:-1])}
                elif datetime_range[0][-1] == 'm':
                    datetime_range_delta = {'minutes': int(datetime_range[0][:-1])}
                elif datetime_range[0][-1] == 'h':
                    datetime_range_delta = {'hours': int(datetime_range[0][:-1])}
                attr_val = (
                    (
                        datetime.datetime.utcnow()
                        + datetime.timedelta(**datetime_range_delta)
                    )
                    .isoformat()
                    .split('T')[1]
                )
            else:
                if datetime_range[0][0] not in ['+', '-']:
                    attr_val = datetime_range[0]
                else:
                    # [REF]: https://stackoverflow.com/a/656394/2393762
                    attr_val = (
                        (
                            datetime.datetime.combine(
                                datetime.date.today(),
                                datetime.time.fromisoformat(datetime_range[1]),
                            )
                            - datetime.timedelta(minutes=1)
                        )
                        .isoformat()
                        .split('T')[1]
                    )
        else:
            attr_val = datetime.datetime.utcnow().isoformat().split('T')[1]
        return attr_val

    if attr_type.type == AttrType.URI_WEB:
        attr_val = f'https://sub.domain.com/page-{math.ceil(random.random() * 10000)}/'
        if attr_type.args['allowed_domains']:
            if attr_type.args['strict_matching']:
                domain = 'sub.domain.com'
            else:
                domain = 'domain.com'
            attr_val = attr_val.replace(
                domain, random.choice(attr_type.args['allowed_domains'])
            )
        return attr_val

    if attr_type.type == AttrType.LITERAL:
        attr_val = random.choice(attr_type.args['literal'])
        return attr_val

    if attr_type.type == AttrType.UNION:
        attr_val = generate_attr_val(attr_type=random.choice(attr_type.args['union']))
        return attr_val

    raise Exception(f'Unknown generator attr \'{attr_type}\'')
