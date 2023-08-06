'''Provides 'call' Utility'''

import asyncio
import copy
import datetime
import inspect
import json
import logging
import re
import sys
import traceback
from typing import (TYPE_CHECKING, Any, Awaitable, Callable, MutableMapping,
                    MutableSequence, Union, cast)

from nawah.classes import Query, Var, app_encoder
from nawah.config import Config
from nawah.enums import Event
from nawah.exceptions import (FuncException, InvalidAttrException,
                              InvalidCallEndpointException,
                              InvalidDocAttrException, InvalidDocException,
                              InvalidFuncException, InvalidModuleException,
                              InvalidQueryAttrException, InvalidQueryException,
                              MissingDocAttrException,
                              MissingQueryAttrException)

from ._cache import _get_cache, _set_cache, reset_cache_channel
from ._check_permissions import check_permissions as check_permissions_utility
from ._val import camel_to_upper, var_value
from ._validate import validate_attr

if TYPE_CHECKING:
    from nawah.classes import Attr
    from nawah.types import (NawahDoc, NawahEnv, NawahEvents, NawahQuery,
                             Results)


logger = logging.getLogger('nawah')


async def call(
    endpoint: str,
    /,
    *,
    module_name: str = None,
    skip_events: 'NawahEvents' = None,
    env: 'NawahEnv' = None,
    query: 'NawahQuery' = None,
    doc: 'NawahDoc' = None,
    args: MutableMapping[str, Any] = None,
) -> 'Results':
    '''Checks validity of an endpoint and calls Nawah Function callable at endpoint,
    returning the couroutine of the callable. If endpoint points to non-existent
    Nawah Function, raises 'InvalidFuncException' '''

    if not re.match(r'^[a-z_]+\/[a-z_]+$', endpoint):
        raise InvalidCallEndpointException(endpoint=endpoint)

    endpoint_module, endpoint_func = endpoint.split('/')

    try:
        module = Config.modules[endpoint_module]
    except KeyError as e:
        raise InvalidModuleException(module_name=endpoint_module) from e

    try:
        func = module.funcs[endpoint_func]
    except KeyError as e:
        raise InvalidFuncException(
            module_name=endpoint_module, func_name=endpoint_func
        ) from e

    # Set defaults for kwargs
    module_name = module_name or endpoint_module
    skip_events = skip_events or []
    query = query or []
    doc = doc or {}
    env = env or {}
    args = args or {}

    # Convert query to Query object
    query = Query(query)

    # Check conditions for call checks
    check_permissions = Event.PERM not in skip_events
    check_attrs_query = Event.ATTRS_QUERY not in skip_events
    check_attrs_doc = Event.ATTRS_DOC not in skip_events
    check_cache = Event.CACHE not in skip_events
    check_analytics = Event.ANALYTICS not in skip_events

    if check_permissions:
        query_mod, doc_mod = check_permissions_utility(func=func, env=env)
        # Use return of check_permissions_utility to update query, doc
        query.append(
            _process_query_mod(
                query=query,
                query_mod=query_mod,
                env=env,
                doc=doc,
            )
        )
        doc.update(
            _process_doc_mod(
                doc=doc,
                doc_mod=doc_mod,
                env=env,
                query=query,
            )
        )

    if check_attrs_query:
        func.query_attrs = cast(MutableSequence, func.query_attrs)
        _check_query_attrs(query=query, query_attrs=func.query_attrs)

    if check_attrs_doc:
        func.doc_attrs = cast(MutableSequence, func.doc_attrs)
        _check_doc_attrs(doc=doc, doc_attrs=func.doc_attrs)

    if check_cache:
        cache_key, call_cache = await _get_cache(
            func=func,
            skip_events=skip_events,
            env=env,
            query=query,
        )

        if call_cache:
            return call_cache

    if check_analytics:
        # [TODO] Implement
        pass

    try:
        func_callable = cast(Callable[..., Awaitable['Results']], func.callable)
        kwargs: MutableMapping = {
            'func': func,
            'module_name': module_name,
            'skip_events': skip_events,
            'env': env,
            'query': query,
            'doc': doc,
        }

        # Iterate over call_args to set values
        for arg_name, arg_type in (func.call_args or {}).items():
            if arg_name not in args:
                kwargs[arg_name] = None
                continue

            try:
                validate_attr(
                    mode='create',
                    attr_name=arg_name,
                    attr_type=arg_type,
                    attr_val=args[arg_name],
                )
            except InvalidAttrException as e:
                raise FuncException(
                    status=500,
                    msg=f'Invalid value for \'Call Arg\' \'{arg_name}\' of \'{module_name}\''
                    f'.\'{func.name}\'',
                    args={'code': 'INVALID_CALL_ARG'},
                ) from e
            # Call Arg value is value, append it to kwargs to be passed to Func callable
            kwargs[arg_name] = args[arg_name]
            # Delete arg_val from args to filter out invalid args
            del args[arg_name]

        # If after iterating over call_args, we still have values in args, declare them invalid
        if args:
            arg_name = list(args)[0]
            raise FuncException(
                status=500,
                msg=f'Function of \'{module_name}\'.\'{func.name}\' does not define \'{arg_name}\' '
                'in \'call_args\'',
                args={'code': 'UNKNOWN_CALL_ARG'},
            )

        results = await func_callable(
            **{
                param: kwargs[param]
                for param in inspect.signature(func_callable).parameters
                if param in kwargs
            }
        )
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()

        logger.error(
            'Callable for \'%s\' failed with Exception of type: %s', endpoint, type(e)
        )
        # [TODO] Check its validity
        logger.debug('Error traceback:')
        for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
            logger.debug('- %s', line)

        if isinstance(e, FuncException):
            raise e

        raise FuncException(
            status=getattr(e, 'status', 500),
            msg=e.args[0] if e.args else 'Unexpected error has occurred',
            args={'code': camel_to_upper(e.__class__.__name__)},
        ) from e

    if 'args' in results and 'session' in results['args']:
        env['session'] = json.loads(app_encoder.encode(results['args']['session']))

    if check_cache and cache_key:
        results['args']['cache_key'] = cache_key
        if 'cache_time' not in results['args']:
            logger.debug(
                'Results generated with \'cache_key\'. Calling \'_set_cache\'.'
            )
            results['args']['cache_time'] = datetime.datetime.utcnow().isoformat()
        # [TODO] Add callback to handle errors
        asyncio.create_task(_set_cache(func=func, cache_key=cache_key, results=results))

    if func.cache_channels_reset:
        for channel in func.cache_channels_reset:
            # [TODO] Add callback to handle errors
            asyncio.create_task(reset_cache_channel(channel))

    return results


def _process_query_mod(
    *,
    query_mod: Union[
        MutableMapping[str, Any], MutableSequence[MutableMapping[str, Any]]
    ],
    env: 'NawahEnv',
    query: 'Query',
    doc: 'NawahDoc',
):
    if not query_mod:
        return {}

    query_mod_processed: Union[
        MutableMapping[str, Any], MutableSequence[MutableMapping[str, Any]]
    ]

    if isinstance(query_mod, list):
        query_mod_processed = []
        for query_mod_child in query_mod:
            query_mod_processed.append(
                _process_query_mod(
                    query_mod=query_mod_child,
                    env=env,
                    query=query,
                    doc=doc,
                )
            )

    elif isinstance(query_mod, dict):
        query_mod_processed = {}
        for attr_name, attr_val in query_mod.items():
            if isinstance(attr_val, (list, dict)):
                query_mod_processed[attr_name] = _process_query_mod(
                    query_mod=attr_val,
                    env=env,
                    query=query,
                    doc=doc,
                )
            elif isinstance(attr_val, Var):
                query_mod_processed[attr_name] = var_value(
                    attr_val, env=env, doc=doc, locale=env['session']['user']['locale']
                )
            else:
                query_mod_processed[attr_name] = copy.deepcopy(attr_val)
    else:
        raise Exception('Unexpected non-list, non-dict value for \'query_mod\'')

    return query_mod_processed


def _process_doc_mod(
    *,
    doc_mod: Union[MutableMapping[str, Any], MutableSequence[MutableMapping[str, Any]]],
    env: 'NawahEnv',
    query: 'Query',
    doc: 'NawahDoc',
):
    if not doc_mod:
        return {}

    doc_mod_processed: Union[
        MutableMapping[str, Any], MutableSequence[MutableMapping[str, Any]]
    ]

    if isinstance(doc_mod, list):
        doc_mod_processed = []
        for doc_mod_child in doc_mod:
            doc_mod_processed.append(
                _process_doc_mod(
                    doc_mod=doc_mod_child,
                    env=env,
                    query=query,
                    doc=doc,
                )
            )

    elif isinstance(doc_mod, dict):
        doc_mod_processed = {}
        for attr_name, attr_val in doc_mod.items():
            if isinstance(attr_val, (list, dict)):
                doc_mod_processed[attr_name] = _process_doc_mod(
                    doc_mod=attr_val,
                    env=env,
                    query=query,
                    doc=doc,
                )
            elif isinstance(attr_val, Var):
                doc_mod_processed[attr_name] = var_value(
                    attr_val, env=env, doc=doc, locale=env['session']['user']['locale']
                )
            else:
                doc_mod_processed[attr_name] = copy.deepcopy(attr_val)
    else:
        raise Exception('Unexpected non-list, non-dict value for \'doc_mod\'')

    return doc_mod_processed


def _check_query_attrs(
    *,
    query: 'Query',
    query_attrs: MutableSequence[MutableMapping[str, 'Attr']],
):
    if not query_attrs:
        return

    query_attrs_sets: MutableSequence[MutableMapping[str, str]] = []

    for query_attrs_set in query_attrs:
        query_attrs_sets.append({})
        try:
            for attr_name, attr_type in query_attrs_set.items():
                if attr_name not in query:
                    query_attrs_sets[-1][attr_name] = 'missing'
                    raise MissingQueryAttrException(attr_name=attr_name)

                for i, attr_val in enumerate(query[attr_name]):
                    try:
                        query[attr_name][i] = validate_attr(
                            mode='create',
                            attr_name=attr_name,
                            attr_type=attr_type,
                            attr_val=attr_val,
                        )
                    except InvalidAttrException as e:
                        query_attrs_sets[-1][attr_name] = 'invalid'
                        raise InvalidQueryAttrException(
                            attr_name=attr_name,
                            attr_type=attr_type,
                            val_type=type(attr_val),
                        ) from e

                query_attrs_sets[-1][attr_name] = 'valid'
            # If looped successfully over complete set, return to indicate valid Query
            return
        except (InvalidAttrException, MissingQueryAttrException):
            # If exception occur, pass it to allow checking all sets
            pass

    # If all sets are checked but failed to return, rase InvalidQueryException
    raise InvalidQueryException(query_attrs_sets=query_attrs_sets)


def _check_doc_attrs(
    *,
    doc: 'NawahDoc',
    doc_attrs: MutableSequence[MutableMapping[str, 'Attr']],
):
    if not doc_attrs:
        return

    doc_attrs_sets: MutableSequence[MutableMapping[str, str]] = []

    for doc_attrs_set in doc_attrs:
        doc_attrs_sets.append({})
        try:
            for attr_name, attr_type in doc_attrs_set.items():
                if attr_name not in doc:
                    doc_attrs_sets[-1][attr_name] = 'missing'
                    raise MissingDocAttrException(attr_name=attr_name)

                try:
                    doc[attr_name] = validate_attr(
                        mode='create',
                        attr_name=attr_name,
                        attr_type=attr_type,
                        attr_val=doc[attr_name],
                    )
                except InvalidAttrException as e:
                    doc_attrs_sets[-1][attr_name] = 'invalid'
                    raise InvalidDocAttrException(
                        attr_name=attr_name,
                        attr_type=attr_type,
                        val_type=type(doc[attr_name]),
                    ) from e

                doc_attrs_sets[-1][attr_name] = 'valid'
            # If looped successfully over complete set, return to indicate valid Doc
            return
        except (InvalidAttrException, MissingDocAttrException):
            # If exception occur, pass it to allow checking all sets
            pass

    # If all sets are checked but failed to return, rase InvalidDocException
    raise InvalidDocException(doc_attrs_sets=doc_attrs_sets)
