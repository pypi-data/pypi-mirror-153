'''Provides 'validate_doc', 'validate_attr' Utilities'''

import copy
import datetime
import inspect
import logging
import re
from math import inf
from typing import TYPE_CHECKING, Any, Literal, MutableMapping, Union, cast

from bson import ObjectId

from nawah.classes import Attr
from nawah.config import Config
from nawah.enums import AttrType, LocaleStrategy
from nawah.exceptions import InvalidAttrException, MissingAttrException

if TYPE_CHECKING:
    from nawah.types import NawahDoc

logger = logging.getLogger('nawah')

file_typed_dict_attr = Attr.TYPED_DICT(
    dict={
        'name': Attr.STR(),
        'lastModified': Attr.INT(),
        'type': Attr.STR(),
        'size': Attr.INT(),
        'ref': Attr.ID(),
    }
)


def validate_doc(
    *,
    mode: Literal['create', 'create_draft', 'update'],
    doc: 'NawahDoc',
    attrs: MutableMapping[str, 'Attr'],
):
    '''Validates 'doc' value against dict of Attr Types dict 'attrs' '''

    attrs_map = {attr.split('.')[0]: attr for attr in doc.keys()}

    for attr in attrs:
        if attr not in attrs_map:
            if mode == 'create':
                doc[attr] = None
            else:
                continue
        elif mode != 'create':
            attr = attrs_map[attr]

        if mode != 'create' and '.' in attr:
            doc[attr] = _validate_dot_notated(
                attr=attr,
                doc=doc,
                attrs=attrs,
            )
        else:
            try:
                doc[attr] = validate_attr(
                    attr_name=attr,
                    attr_type=attrs[attr],
                    attr_val=doc[attr],
                    mode=mode,
                    doc=doc,
                )
            except Exception as e:
                if doc[attr] is None:
                    raise MissingAttrException(attr_name=attr) from e

                raise InvalidAttrException(
                    attr_name=attr, attr_type=attrs[attr], val_type=type(doc[attr])
                ) from e


def _validate_dot_notated(
    attr: str,
    doc: 'NawahDoc',
    attrs: MutableMapping[str, 'Attr'],
):
    '''Validates value of dot-notated 'attr' against Attr Type'''

    attr_path = attr.split('.')
    attr_path_len = len(attr_path)
    attr_type: Union[MutableMapping[str, 'Attr'], 'Attr'] = attrs

    try:
        for i in range(attr_path_len):
            # Iterate over attr_path to reach last valid Attr Type
            if not isinstance(attr_type, Attr):
                attr_type = cast(MutableMapping[str, 'Attr'], attr_type)

                attr_type = attr_type[attr_path[i]]
            elif isinstance(attr_type, Attr):
                attr_type = cast('Attr', attr_type)

                if attr_type.type == AttrType.ANY:
                    return doc[attr]

                if attr_type.type == AttrType.LOCALE:
                    if attr_path[i] not in Config.locales:
                        raise Exception()
                    attr_type = Attr.STR()
                elif attr_type.type == AttrType.TYPED_DICT:
                    attr_type = attr_type.args['dict'][attr_path[i]]
                elif attr_type.type == AttrType.KV_DICT:
                    attr_type = attr_type.args['val']
                # However, if list or union, start a new _validate_dot_notated call as it is required to check all the provided types
                elif attr_type.type in [AttrType.LIST, AttrType.UNION]:
                    if attr_type.type == AttrType.LIST:
                        attr_type_iter = attr_type.args['list']
                    else:
                        attr_type_iter = attr_type.args['union']
                    for child_attr_type in attr_type_iter:
                        attr_val = _validate_dot_notated(
                            attr='.'.join(attr_path[i:]),
                            doc={'.'.join(attr_path[i:]): doc[attr]},
                            attrs={attr_path[i]: child_attr_type},
                        )
                        if attr_val is not None:
                            return attr_val
                    raise Exception()
                else:
                    raise Exception()
            else:
                raise Exception()

        # Validate val against final Attr Type
        # mode is statically set to update as dot-notation attrs are only allowed in update calls
        attr_val = validate_attr(
            mode='update',
            attr_name=attr,
            attr_type=cast('Attr', attr_type),
            attr_val=doc[attr],
            doc=doc,
        )
        return attr_val
    except Exception as e:
        raise InvalidAttrException(
            attr_name=attr, attr_type=attrs[attr_path[0]], val_type=type(doc[attr])
        ) from e


def validate_attr(
    *,
    mode: Literal['create', 'create_draft', 'update', 'deep'],
    attr_name: str,
    attr_type: 'Attr',
    attr_val: Any,
    doc: 'NawahDoc' = None,
):
    '''Validates value 'attr_val' against Attr Type 'attr_type'. Returns processed valid
    value, if valid, otherwise raises 'InvalidAttrException' '''

    # Basic checks for None-value
    if attr_val is None:
        # For mode==update, having None-value is accepted
        if mode == 'update':
            return None
        # Otherwise check for default
        if attr_type.default:
            # If default.value is callable, call with doc to generate value
            if callable(attr_type.default.value):
                return attr_type.default.value(doc)
            # Else, return copy from default.value (to avoid passing objects)
            return copy.deepcopy(attr_type.default.value)

    attr_oper: Literal[
        None, '$add', '$multiply', '$append', '$set_index', '$del_val', '$del_index'
    ] = None
    attr_oper_args = {}
    if mode == 'update' and isinstance(attr_val, dict):
        if '$add' in attr_val.keys():
            attr_oper = '$add'
            if '$field' in attr_val.keys() and attr_val['$field']:
                attr_oper_args['$field'] = attr_val['$field']
            else:
                attr_oper_args['$field'] = None
            attr_val = attr_val['$add']
        elif '$multiply' in attr_val.keys():
            attr_oper = '$multiply'
            if '$field' in attr_val.keys() and attr_val['$field']:
                attr_oper_args['$field'] = attr_val['$field']
            else:
                attr_oper_args['$field'] = None
            attr_val = attr_val['$multiply']
        elif '$append' in attr_val.keys():
            attr_oper = '$append'
            if '$unique' in attr_val.keys() and attr_val['$unique'] == True:
                attr_oper_args['$unique'] = True
            else:
                attr_oper_args['$unique'] = False
            attr_val = [attr_val['$append']]
        elif '$set_index' in attr_val.keys():
            attr_oper = '$set_index'
            attr_oper_args['$index'] = attr_val['$index']
            attr_val = [attr_val['$set_index']]
        elif '$del_val' in attr_val.keys():
            attr_oper = '$del_val'
            attr_val = attr_val['$del_val']
            if attr_type.type != 'LIST' or type(attr_val) != list:
                raise InvalidAttrException(
                    attr_name=attr_name, attr_type=attr_type, val_type=type(attr_val)
                )
            return return_valid_attr(
                attr_val=attr_val, attr_oper=attr_oper, attr_oper_args=attr_oper_args
            )
        elif '$del_index' in attr_val.keys():
            attr_oper = '$del_index'
            attr_oper_args['$index'] = attr_val['$del_index']
            attr_val = attr_val['$del_index']
            if (attr_type.type == AttrType.LIST and type(attr_val) == int) or (
                attr_type.type == AttrType.KV_DICT and type(attr_val) == str
            ):
                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )
            else:
                raise InvalidAttrException(
                    attr_name=attr_name, attr_type=attr_type, val_type=type(attr_val)
                )

    # Deepcopy attr_val to eliminate changes in in original object
    attr_val = copy.deepcopy(attr_val)

    if attr_type.type == AttrType.ANY:
        if attr_val is not None:
            return return_valid_attr(
                attr_val=attr_val,
                attr_oper=attr_oper,
                attr_oper_args=attr_oper_args,
            )

    elif attr_type.type == AttrType.BOOL:
        if type(attr_val) == bool:
            return return_valid_attr(
                attr_val=attr_val,
                attr_oper=attr_oper,
                attr_oper_args=attr_oper_args,
            )

    elif attr_type.type == AttrType.DATE:
        if isinstance(attr_val, str) and re.match(
            r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$', attr_val
        ):
            if attr_type.args['ranges']:
                for date_range in attr_type.args['ranges']:
                    date_range = copy.deepcopy(date_range)
                    for i in [0, 1]:
                        if date_range[i][0] in ['+', '-']:
                            date_range_delta = {}
                            if date_range[i][-1] == 'd':
                                date_range_delta = {'days': int(date_range[i][:-1])}
                            elif date_range[i][-1] == 'w':
                                date_range_delta = {'weeks': int(date_range[i][:-1])}
                            date_range[i] = (
                                (
                                    datetime.datetime.utcnow()
                                    + datetime.timedelta(**date_range_delta)
                                )
                                .isoformat()
                                .split('T')[0]
                            )
                    if attr_val >= date_range[0] and attr_val < date_range[1]:
                        return return_valid_attr(
                            attr_val=attr_val,
                            attr_oper=attr_oper,
                            attr_oper_args=attr_oper_args,
                        )
            else:
                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )

    elif attr_type.type == AttrType.DATETIME:
        if isinstance(attr_val, str) and re.match(
            r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}(:[0-9]{2}(\.[0-9]{6})?)?$',
            attr_val,
        ):
            if attr_type.args['ranges']:
                for datetime_range in attr_type.args['ranges']:
                    datetime_range = copy.deepcopy(datetime_range)
                    for i in [0, 1]:
                        if datetime_range[i][0] in ['+', '-']:
                            datetime_range_delta = {}
                            if datetime_range[i][-1] == 'd':
                                datetime_range_delta = {
                                    'days': int(datetime_range[i][:-1])
                                }
                            elif datetime_range[i][-1] == 's':
                                datetime_range_delta = {
                                    'seconds': int(datetime_range[i][:-1])
                                }
                            elif datetime_range[i][-1] == 'm':
                                datetime_range_delta = {
                                    'minutes': int(datetime_range[i][:-1])
                                }
                            elif datetime_range[i][-1] == 'h':
                                datetime_range_delta = {
                                    'hours': int(datetime_range[i][:-1])
                                }
                            elif datetime_range[i][-1] == 'w':
                                datetime_range_delta = {
                                    'weeks': int(datetime_range[i][:-1])
                                }
                            datetime_range[i] = (
                                datetime.datetime.utcnow()
                                + datetime.timedelta(**datetime_range_delta)
                            ).isoformat()
                    if attr_val >= datetime_range[0] and attr_val < datetime_range[1]:
                        return return_valid_attr(
                            attr_val=attr_val,
                            attr_oper=attr_oper,
                            attr_oper_args=attr_oper_args,
                        )
            else:
                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )

    elif attr_type.type == AttrType.ATTR:
        if isinstance(attr_val, dict):
            # [TODO] Clean-up to import this on root level
            from .._attr_type import decode_attr_type

            decode_attr_type(encoded_attr_type=attr_val)
            return return_valid_attr(
                attr_val=attr_val,
                attr_oper=attr_oper,
                attr_oper_args=attr_oper_args,
            )

    elif attr_type.type == AttrType.KV_DICT:
        if type(attr_val) == dict:
            if attr_type.args['len_range']:
                if not (
                    attr_type.args['len_range'][0]
                    <= len(attr_val.keys())
                    < attr_type.args['len_range'][1]
                ):
                    raise InvalidAttrException(
                        attr_name=attr_name,
                        attr_type=attr_type,
                        val_type=type(attr_val),
                    )
            if attr_type.args['req']:
                for req_key in attr_type.args['req']:
                    if req_key not in attr_val.keys():
                        raise InvalidAttrException(
                            attr_name=attr_name,
                            attr_type=attr_type,
                            val_type=type(attr_val),
                        )
            shadow_attr_val = {}
            try:
                for child_attr_val in attr_val.keys():
                    shadow_attr_val[
                        validate_attr(
                            mode='deep',
                            attr_name=f'{attr_name}.{child_attr_val}',
                            attr_type=attr_type.args['key'],
                            attr_val=child_attr_val,
                            doc=doc,
                        )
                    ] = validate_attr(
                        mode='deep',
                        attr_name=f'{attr_name}.{child_attr_val}',
                        attr_type=attr_type.args['val'],
                        attr_val=attr_val[child_attr_val],
                        doc=doc,
                    )
                return return_valid_attr(
                    attr_val=shadow_attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )
            except InvalidAttrException:
                pass

    elif attr_type.type == AttrType.TYPED_DICT:
        if type(attr_val) == dict:
            try:
                for child_attr_type in attr_type.args['dict'].keys():
                    if child_attr_type not in attr_val.keys():
                        attr_val[child_attr_type] = None
                    attr_val[child_attr_type] = validate_attr(
                        mode='deep',
                        attr_name=f'{attr_name}.{child_attr_type}',
                        attr_type=attr_type.args['dict'][child_attr_type],
                        attr_val=attr_val[child_attr_type],
                        doc=doc,
                    )
                # Match keys _after_ checking child attrs in order to allow _validate_default to run on all child attrs
                if set(attr_val.keys()) != set(attr_type.args['dict'].keys()):
                    raise InvalidAttrException(
                        attr_name=attr_name,
                        attr_type=attr_type,
                        val_type=type(attr_val),
                    )

                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )
            except InvalidAttrException:
                pass

    elif attr_type.type == AttrType.EMAIL:
        if type(attr_val) == str and re.match(r'^[^@]+@[^@]+\.[^@]+$', attr_val):
            if attr_type.args['allowed_domains']:
                for domain in attr_type.args['allowed_domains']:
                    if attr_type.args['strict_matching']:
                        domain = f'@{domain}'
                    if attr_val.endswith(domain):
                        return return_valid_attr(
                            attr_val=attr_val,
                            attr_oper=attr_oper,
                            attr_oper_args=attr_oper_args,
                        )
            elif attr_type.args['disallowed_domains']:
                for domain in attr_type.args['disallowed_domains']:
                    if attr_type.args['strict_matching']:
                        domain = f'@{domain}'
                    if attr_val.endswith(domain):
                        break
                else:
                    return return_valid_attr(
                        attr_val=attr_val,
                        attr_oper=attr_oper,
                        attr_oper_args=attr_oper_args,
                    )
            else:
                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )

    elif attr_type.type == AttrType.FILE:
        try:
            if isinstance(attr_val, list) and len(attr_val):
                attr_val = validate_attr(
                    mode='deep',
                    attr_name=attr_name,
                    attr_type=attr_type,
                    attr_val=attr_val[0],
                    doc=doc,
                )

            validate_attr(
                mode='create',
                attr_name=attr_name,
                attr_type=file_typed_dict_attr,
                attr_val=attr_val,
            )

            return return_valid_attr(
                attr_val=attr_val,
                attr_oper=attr_oper,
                attr_oper_args=attr_oper_args,
            )

        except InvalidAttrException:
            pass

    elif attr_type.type == AttrType.BYTES:
        if isinstance(attr_val, bytes):
            return return_valid_attr(
                attr_val=attr_val,
                attr_oper=attr_oper,
                attr_oper_args=attr_oper_args,
            )

    elif attr_type.type == AttrType.FLOAT:
        if isinstance(attr_val, str) and re.match(r'^[0-9]+(\.[0-9]+)?$', attr_val):
            attr_val = float(attr_val)
        elif isinstance(attr_val, int):
            attr_val = float(attr_val)

        if isinstance(attr_val, float):
            if attr_type.args['ranges']:
                for _range in attr_type.args['ranges']:
                    if _range[0] <= attr_val < _range[1]:
                        return return_valid_attr(
                            attr_val=attr_val,
                            attr_oper=attr_oper,
                            attr_oper_args=attr_oper_args,
                        )
            else:
                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )

    elif attr_type.type == AttrType.GEO_POINT:
        if (
            isinstance(attr_val, dict)
            and set(attr_val.keys()) == {'type', 'coordinates'}
            and attr_val['type'] in ['Point']
            and isinstance(attr_val['coordinates'], list)
            and len(attr_val['coordinates']) == 2
            and type(attr_val['coordinates'][0]) in [int, float]
            and type(attr_val['coordinates'][1]) in [int, float]
        ):
            return return_valid_attr(
                attr_val=attr_val,
                attr_oper=attr_oper,
                attr_oper_args=attr_oper_args,
            )

    elif attr_type.type == AttrType.ID:
        if isinstance(attr_val, dict) and '_id' in attr_val:
            return return_valid_attr(
                attr_val=str(attr_val['_id']),
                attr_oper=attr_oper,
                attr_oper_args=attr_oper_args,
            )

        if isinstance(attr_val, ObjectId):
            return return_valid_attr(
                attr_val=str(attr_val),
                attr_oper=attr_oper,
                attr_oper_args=attr_oper_args,
            )

        if isinstance(attr_val, str):
            try:
                if not re.match(r'^[a-f0-9]{24}$', attr_val):
                    raise InvalidAttrException(
                        attr_name=attr_name, attr_type=attr_type, val_type=str
                    )

                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )
            except InvalidAttrException:
                pass

    elif attr_type.type == AttrType.INT:
        if isinstance(attr_val, str) and re.match(r'^[0-9]+$', attr_val):
            attr_val = int(attr_val)

        if isinstance(attr_val, int):
            if attr_type.args['ranges']:
                # [TODO] Implement inf range, ref: https://stackoverflow.com/questions/9884213/looping-from-1-to-infinity-in-python
                for _range in attr_type.args['ranges']:
                    if attr_val in range(*_range):
                        return return_valid_attr(
                            attr_val=attr_val,
                            attr_oper=attr_oper,
                            attr_oper_args=attr_oper_args,
                        )
            else:
                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )

    elif attr_type.type == AttrType.IP:
        if isinstance(attr_val, str) and re.match(
            r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
            attr_val,
        ):
            return return_valid_attr(
                attr_val=attr_val,
                attr_oper=attr_oper,
                attr_oper_args=attr_oper_args,
            )

    elif attr_type.type == AttrType.LIST:
        if isinstance(attr_val, list):
            try:
                if attr_type.args['len_range']:
                    if not (
                        attr_type.args['len_range'][0]
                        <= len(attr_val)
                        < attr_type.args['len_range'][1]
                    ):
                        raise InvalidAttrException(
                            attr_name=attr_name,
                            attr_type=attr_type,
                            val_type=type(attr_val),
                        )
                for i, child_attr_val in enumerate(attr_val):
                    child_attr_check = False
                    for child_attr_type in attr_type.args['list']:
                        try:
                            attr_val[i] = validate_attr(
                                mode='deep',
                                attr_name=attr_name,
                                attr_type=child_attr_type,
                                attr_val=child_attr_val,
                                doc=doc,
                            )
                            child_attr_check = True
                            break
                        except InvalidAttrException:
                            pass

                    if not child_attr_check:
                        raise InvalidAttrException(
                            attr_name=attr_name,
                            attr_type=attr_type,
                            val_type=type(attr_val),
                        )
                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )
            except InvalidAttrException:
                pass

    elif attr_type.type == AttrType.LOCALE:
        try:
            attr_val = validate_attr(
                mode='deep',
                attr_name=attr_name,
                attr_type=Attr.KV_DICT(
                    key=Attr.LITERAL(literal=copy.copy(Config.locales)),
                    val=Attr.STR(),
                    len_range=[1, inf],
                    req=[Config.locale],
                ),
                attr_val=attr_val,
                doc=doc,
            )
            if Config.locale_strategy == LocaleStrategy.NONE_VALUE:
                attr_val = {
                    locale: attr_val[locale] if locale in attr_val.keys() else None
                    for locale in Config.locales
                }
            elif callable(Config.locale_strategy):
                attr_val = {
                    locale: attr_val[locale]
                    if locale in attr_val.keys()
                    else Config.locale_strategy(attr_val=attr_val, locale=locale)
                    for locale in Config.locales
                }
            else:
                attr_val = {
                    locale: attr_val[locale]
                    if locale in attr_val.keys()
                    else attr_val[Config.locale]
                    for locale in Config.locales
                }
            return return_valid_attr(
                attr_val=attr_val, attr_oper=attr_oper, attr_oper_args=attr_oper_args
            )
        except InvalidAttrException:
            pass

    elif attr_type.type == AttrType.LOCALES:
        if attr_val in Config.locales:
            return return_valid_attr(
                attr_val=attr_val,
                attr_oper=attr_oper,
                attr_oper_args=attr_oper_args,
            )

    elif attr_type.type == AttrType.PHONE:
        if isinstance(attr_val, str):
            if attr_type.args['codes']:
                for phone_code in attr_type.args['codes']:
                    if re.match(fr'^\+{phone_code}[0-9]+$', attr_val):
                        return return_valid_attr(
                            attr_val=attr_val,
                            attr_oper=attr_oper,
                            attr_oper_args=attr_oper_args,
                        )
            else:
                if re.match(r'^\+[0-9]+$', attr_val):
                    return return_valid_attr(
                        attr_val=attr_val,
                        attr_oper=attr_oper,
                        attr_oper_args=attr_oper_args,
                    )

    elif attr_type.type == AttrType.STR:
        if isinstance(attr_val, str):
            if attr_type.args['pattern']:
                if re.match(f'^{attr_type.args["pattern"]}$', attr_val):
                    return return_valid_attr(
                        attr_val=attr_val,
                        attr_oper=attr_oper,
                        attr_oper_args=attr_oper_args,
                    )
            else:
                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )

    elif attr_type.type == AttrType.TIME:
        if isinstance(attr_val, str) and re.match(
            r'^[0-9]{2}:[0-9]{2}(:[0-9]{2}(\.[0-9]{6})?)?$', attr_val
        ):
            if attr_type.args['ranges']:
                for time_range in attr_type.args['ranges']:
                    time_range = copy.deepcopy(time_range)
                    for i in [0, 1]:
                        if time_range[i][0] in ['+', '-']:
                            time_range_delta = {}
                            if time_range[i][-1] == 's':
                                time_range_delta = {'seconds': int(time_range[i][:-1])}
                            elif time_range[i][-1] == 'm':
                                time_range_delta = {'minutes': int(time_range[i][:-1])}
                            elif time_range[i][-1] == 'h':
                                time_range_delta = {'hours': int(time_range[i][:-1])}
                            time_range[i] = (
                                (
                                    datetime.datetime.utcnow()
                                    + datetime.timedelta(**time_range_delta)
                                )
                                .isoformat()
                                .split('T')[1]
                            )
                    if time_range[1] > attr_val >= time_range[0]:
                        return return_valid_attr(
                            attr_val=attr_val,
                            attr_oper=attr_oper,
                            attr_oper_args=attr_oper_args,
                        )
            else:
                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )

    elif attr_type.type == AttrType.URI_WEB:
        if isinstance(attr_val, str) and re.match(
            r'^https?:\/\/(?:[\w\-\_]+\.)(?:\.?[\w]{2,})+([\?\/].*)?$', attr_val
        ):
            if attr_type.args['allowed_domains']:
                attr_val_domain = attr_val.split('/')[2]
                for domain in attr_type.args['allowed_domains']:
                    if attr_type.args['strict_matching'] and attr_val_domain == domain:
                        return return_valid_attr(
                            attr_val=attr_val,
                            attr_oper=attr_oper,
                            attr_oper_args=attr_oper_args,
                        )

                    if not attr_type.args[
                        'strict_matching'
                    ] and attr_val_domain.endswith(domain):
                        return return_valid_attr(
                            attr_val=attr_val,
                            attr_oper=attr_oper,
                            attr_oper_args=attr_oper_args,
                        )
            elif attr_type.args['disallowed_domains']:
                attr_val_domain = attr_val.split('/')[2]
                for domain in attr_type.args['disallowed_domains']:
                    if attr_type.args['strict_matching'] and attr_val_domain == domain:
                        break

                    if not attr_type.args[
                        'strict_matching'
                    ] and attr_val_domain.endswith(domain):
                        break
                else:
                    return return_valid_attr(
                        attr_val=attr_val,
                        attr_oper=attr_oper,
                        attr_oper_args=attr_oper_args,
                    )
            else:
                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )

    elif attr_type.type == AttrType.LITERAL:
        if attr_val in attr_type.args['literal']:
            return return_valid_attr(
                attr_val=attr_val,
                attr_oper=attr_oper,
                attr_oper_args=attr_oper_args,
            )

    elif attr_type.type == AttrType.UNION:
        child_attr_check = False
        for child_attr in attr_type.args['union']:
            try:
                attr_val = validate_attr(
                    mode='deep',
                    attr_name=attr_name,
                    attr_type=child_attr,
                    attr_val=attr_val,
                    doc=doc,
                )
                child_attr_check = True
            except InvalidAttrException:
                continue

            if child_attr_check:
                return return_valid_attr(
                    attr_val=attr_val,
                    attr_oper=attr_oper,
                    attr_oper_args=attr_oper_args,
                )

    elif attr_type.type == AttrType.TYPE:
        try:
            func_params = {
                'mode': mode,
                'attr_name': attr_name,
                'attr_type': attr_type,
                'attr_val': attr_val,
            }
            attr_val = attr_type.args['func'](
                **{
                    param: func_params[param]
                    for param in inspect.signature(attr_type.args['func']).parameters
                }
            )
            return return_valid_attr(
                attr_val=attr_val,
                attr_oper=attr_oper,
                attr_oper_args=attr_oper_args,
            )
        except InvalidAttrException:
            pass

    # If no case is matched, check mode, default
    # For mode==update, having None-value is accepted
    if mode == 'update':
        return None
    # Otherwise check for default
    if attr_type.default:
        # If default.value is callable, call with doc to generate value
        if callable(attr_type.default.value):
            return attr_type.default.value(doc)
        # Else, return copy from default.value (to avoid passing objects)
        return copy.deepcopy(attr_type.default.value)

    # If no case is matched, raise
    raise InvalidAttrException(
        attr_name=attr_name, attr_type=attr_type, val_type=type(attr_val)
    )


def return_valid_attr(
    *,
    attr_val: Any,
    attr_oper: Literal[
        None, '$add', '$multiply', '$append', '$set_index', '$del_val', '$del_index'
    ],
    attr_oper_args: MutableMapping[str, Any],
) -> Any:
    if not attr_oper:
        return attr_val

    if attr_oper in ['$add', '$multiply']:
        return {attr_oper: attr_val, '$field': attr_oper_args['$field']}

    if attr_oper == '$del_val':
        return {attr_oper: attr_val}

    if attr_oper == '$append':
        return {'$append': attr_val[0], '$unique': attr_oper_args['$unique']}

    if attr_oper == '$set_index':
        return {'$set_index': attr_val[0], '$index': attr_oper_args['$index']}

    if attr_oper == '$del_index':
        return {'$del_index': attr_oper_args['$index']}
