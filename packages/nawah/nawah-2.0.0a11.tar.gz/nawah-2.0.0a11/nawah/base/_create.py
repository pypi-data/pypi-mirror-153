'''Provides 'create' Base Function callable'''

import asyncio
import datetime
import logging
import sys
import traceback
from functools import partial
from typing import TYPE_CHECKING, Any, MutableSequence, Optional, cast

import nawah.data as Data
from nawah.config import Config
from nawah.enums import Event
from nawah.utils import call, expand_val, validate_doc

from .exceptions import (DuplicateUniqueException, NoDocCreatedException,
                         UtilityModuleDataCallException)

if TYPE_CHECKING:
    from asyncio.futures import Future

    from nawah.types import NawahDoc, NawahEnv, NawahEvents, Results

logger = logging.getLogger('nawah')


async def create(
    *,
    module_name: str,
    skip_events: 'NawahEvents',
    env: 'NawahEnv',
    doc: 'NawahDoc',
    raise_no_success: Optional[bool],
) -> 'Results':
    '''Creates doc for a module'''

    module = Config.modules[module_name]

    if not module.collection:
        raise UtilityModuleDataCallException(
            module_name=module_name, func_name='create'
        )

    # Expand dot-notated keys onto dicts
    doc = expand_val(doc=doc)
    # Deleted all extra doc args
    doc = {
        attr: doc[attr]
        for attr in ['_id', *module.attrs]
        if attr in doc and doc[attr] is not None
    }
    # Append host_add, user_agent, create_time, if present in attrs
    if (
        'user' in module.attrs
        and 'host_add' not in doc
        and env['session']
        and Event.ATTRS_DOC not in skip_events
    ):
        doc['user'] = env['session']['user']['_id']
    if 'create_time' in module.attrs:
        doc['create_time'] = datetime.datetime.utcnow().isoformat()
    if 'host_add' in module.attrs and 'host_add' not in doc:
        doc['host_add'] = env['REMOTE_ADDR']
    if 'user_agent' in module.attrs and 'user_agent' not in doc:
        doc['user_agent'] = env['HTTP_USER_AGENT']
    if Event.ATTRS_DOC not in skip_events:
        # Check presence and validate all attrs in doc args
        validate_doc(
            mode='create',
            doc=doc,
            attrs=module.attrs,
        )
        # Check unique_attrs
        if module.unique_attrs:
            unique_attrs_query: MutableSequence[Any] = [[]]
            for attr in module.unique_attrs:
                if isinstance(attr, str):
                    attr = cast(str, attr)
                    unique_attrs_query[0].append({attr: doc[attr]})
                elif isinstance(attr, tuple):
                    unique_attrs_query[0].append(
                        {child_attr: doc[child_attr] for child_attr in attr}
                    )
                # [TODO] Implement use of single-item dict with LITERAL Attr Type for dynamic unique check based on doc value
            unique_attrs_query.append({'$limit': 1})
            unique_results = await call(
                'base/read',
                module_name=module_name,
                skip_events=[Event.PERM],
                env=env,
                query=unique_attrs_query,
            )
            if unique_results['args']['count']:
                raise DuplicateUniqueException(unique_attrs=module.unique_attrs)

    # Check for counters, to update doc
    if module.counters:
        counter_name: str
        counter_count: int
        counter_value: str
        counter_locks: dict[str, str] = {}
        counter_create: list[str] = []
        counter_update: list[str] = []

        for attr_name, counter in module.counters.items():
            # Counter.counter can be str or callable. Per type figure out lock name
            if isinstance(counter.counter, str):
                counter_name = f'__COUNTER:{counter.counter}'
            elif callable(counter.counter):
                counter_name = counter.counter(doc)

            # Obtain lock for counter_name to prevent duplicates
            counter_lock_results = await call(
                'base/obtain_lock',
                module_name='setting',
                skip_events=[Event.PERM],
                env=env,
                doc={'tags': [counter_name], 'attempts': 3},
            )
            # Add lock_id to counter_locks to delete later
            counter_locks[counter_name] = counter_lock_results['args']['docs'][0]['_id']

            # Read counter value
            counter_results = await call(
                'setting/read',
                skip_events=[Event.PERM],
                env=env,
                query=[{'type': 'global', 'var': counter_name}],
            )
            # At this point, it is possible, counter was never created. Handle that scenario
            if counter_results['args']['count'] == 0:
                # Append counter_name to counter_create so later we create it instead of updating
                # its value
                counter_create.append(counter_name)
                # And, set counter_count explicitly to 1
                counter_count = 1
            else:
                # Otherwise, add to counter_update, and add to current val
                counter_update.append(counter_name)
                counter_count = counter_results['args']['docs'][0]['val'] + 1

            # Pass counter_count to Counter.pattern_formatter to get counter_value to be used in doc
            counter_value = counter.pattern_formatter(counter_count)
            doc[attr_name] = counter_value

    # Execute Data driver create
    results = await Data.create(env=env, collection_name=module.collection, doc=doc)

    # After successfully creating doc, create, update counters and delete locks
    # We will do this asynchronously so we don't hold response of call
    if module.counters:
        for counter_name in counter_create:
            counter_call_task = asyncio.create_task(
                call(
                    'setting/create',
                    skip_events=[Event.PERM],
                    env=env,
                    doc={
                        'type': 'global',
                        'var': counter_name,
                        'val_type': {'type': 'INT', 'args': {}},
                        'val': 1,
                    },
                    args={'raise_no_success': True},
                )
            )
            counter_call_task.add_done_callback(
                partial(
                    _counter_call_callback,
                    env=env,
                    counter_name=counter_name,
                    counter_lock=counter_locks[counter_name],
                )
            )

        for counter_name in counter_update:
            counter_call_task = asyncio.create_task(
                call(
                    'setting/update',
                    # Skip Event ATTRS_QUERY to avoid additional requirements in query
                    skip_events=[Event.PERM, Event.ATTRS_QUERY],
                    env=env,
                    query=[{'var': counter_name}],
                    doc={
                        'val': {'$add': 1},
                    },
                    args={'raise_no_success': True},
                )
            )
            counter_call_task.add_done_callback(
                partial(
                    _counter_call_callback,
                    env=env,
                    counter_name=counter_name,
                    counter_lock=counter_locks[counter_name],
                )
            )

    # create soft action is to only return the new created doc _id.
    if Event.SOFT in skip_events:
        read_results = await call(
            'base/read',
            module_name=module_name,
            skip_events=[Event.PERM],
            env=env,
            query=[[{'_id': results['docs'][0]}]],
        )
        results = read_results['args']

    if raise_no_success is True and results['count'] == 0:
        raise NoDocCreatedException(module_name=module_name)

    return {'status': 200, 'msg': f'Created {results["count"]} docs', 'args': results}


def _counter_call_callback(
    counter_call_task: 'Future',
    env: 'NawahEnv',
    counter_name: str,
    counter_lock: str,
):
    try:
        # Assert we have good call
        counter_call_task.result()
        # Then, delete counter_lock
        delete_lock_call_task = asyncio.create_task(
            call(
                'base/delete_lock',
                module_name='setting',
                skip_events=[Event.PERM],
                env=env,
                query=[{'_id': counter_lock}],
            )
        )
        delete_lock_call_task.add_done_callback(
            partial(
                _delete_lock_call_callback,
                counter_name=counter_name,
                counter_lock=counter_lock,
            )
        )
    except Exception:  # pylint: disable=broad-except
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.error(
            'Call \'setting/[create|update]\' for counter \'%s\' has failed',
            counter_name,
        )
        logger.error(
            'Lock will remain enact to prevent the counter from being reused while it is '
            'not created/updated'
        )
        logger.debug('Error traceback:')
        for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
            logger.error('- %s', line)


def _delete_lock_call_callback(
    delete_lock_call_task: 'Future',
    counter_name: str,
    counter_lock: str,
):
    try:
        # Assert we have good call
        delete_lock_call_task.result()
    except Exception:  # pylint: disable=broad-except
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.error(
            'Call \'base/delete_lock\' for counter \'%s\' with \'_id\' \'%s\' has failed. DELETE '
            'MANUALLY NOW',
            counter_name,
            counter_lock,
        )
        logger.debug('Error traceback:')
        for line in traceback.format_exception(exc_type, exc_value, exc_traceback):
            logger.error('- %s', line)
