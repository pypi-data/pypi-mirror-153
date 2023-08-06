'''Provides 'user' Module Functions callables'''

from typing import TYPE_CHECKING, Optional

from bson import ObjectId

from nawah.config import Config
from nawah.enums import Event
from nawah.exceptions import FuncException
from nawah.utils import call

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahDoc, NawahEnv, NawahEvents, Results


async def _read(
    skip_events: 'NawahEvents',
    env: 'NawahEnv',
    query: 'Query',
    skip_sanitise_results: Optional[bool],
) -> 'Results':
    skip_events.append(Event.PERM)
    read_results = await call(
        'base/read', module_name='user', skip_events=skip_events, env=env, query=query
    )

    if read_results['status'] != 200:
        return read_results

    # Return results as is if both sanitise_results, user_settings are to be skipped
    if skip_sanitise_results is True:
        return read_results

    # Otherwise, iterate over results and apply not skipped action
    for i, _ in enumerate(read_results['args']['docs']):
        user = read_results['args']['docs'][i]
        # Apply sanitise_results, removing hashes, if not skipped
        if skip_sanitise_results is not True:
            for user_attr_sanitise in Config.user_attrs_sanitise:
                del user[user_attr_sanitise]

    return read_results


async def _create(
    skip_events: 'NawahEvents', env: 'NawahEnv', doc: 'NawahDoc'
) -> 'Results':
    if Event.ATTRS_DOC not in skip_events:
        doc['groups'] = [ObjectId('f00000000000000000000013')]

    create_results = await call(
        'base/create', skip_events=[Event.PERM], module_name='user', env=env, doc=doc
    )

    return create_results


async def _read_privileges(env: 'NawahEnv', query: 'Query') -> 'Results':
    # Confirm _id is valid
    results = await call(
        'user/read',
        skip_events=[Event.PERM],
        env=env,
        query=[{'_id': query['_id'][0]}],
        args={'skip_sanitise_results': True},
    )
    if not results['args']['count']:
        raise FuncException(
            status=400, msg='User is invalid.', args={'code': 'INVALID_USER'}
        )
    user = results['args']['docs'][0]
    for group in user['groups']:
        group_results = await call(
            'group/read', skip_events=[Event.PERM], env=env, query=[{'_id': group}]
        )
        group = group_results['args']['docs'][0]
        for privilege in group['privileges'].keys():
            if privilege not in user['privileges'].keys():
                user['privileges'][privilege] = []
            for i in range(len(group['privileges'][privilege])):
                if (
                    group['privileges'][privilege][i]
                    not in user['privileges'][privilege]
                ):
                    user['privileges'][privilege].append(
                        group['privileges'][privilege][i]
                    )
    return results


async def _add_group(
    skip_events: 'NawahEvents', env: 'NawahEnv', query: 'Query', doc: 'NawahDoc'
) -> 'Results':
    # Check for list group attr
    if isinstance(doc['group'], list):
        for i in range(0, len(doc['group']) - 1):
            await call(
                'user/add_group',
                skip_events=skip_events,
                env=env,
                query=query,
                doc={'group': doc['group'][i]},
            )
        doc['group'] = doc['group'][-1]
    # Confirm all basic args are provided
    doc['group'] = ObjectId(doc['group'])
    # Confirm group is valid
    results = await call(
        'group/read', skip_events=[Event.PERM], env=env, query=[{'_id': doc['group']}]
    )
    if not results['args']['count']:
        raise FuncException(
            status=400, msg='Group is invalid.', args={'code': 'INVALID_GROUP'}
        )
    # Get user details
    results = await call('user/read', skip_events=[Event.PERM], env=env, query=query)
    if not results['args']['count']:
        raise FuncException(
            status=400, msg='User is invalid.', args={'code': 'INVALID_USER'}
        )
    user = results['args']['docs'][0]
    # Confirm group was not added before
    if doc['group'] in user['groups']:
        raise FuncException(
            status=400,
            msg='User is already a member of the group.',
            args={'code': 'GROUP_ADDED'},
        )
    user['groups'].append(doc['group'])
    # Update the user
    results = await call(
        'user/update',
        skip_events=[Event.PERM],
        env=env,
        query=query,
        doc={'groups': user['groups']},
    )
    # if update fails, return update results
    if results['status'] != 200:
        return results
    # Check if the updated User doc belongs to current session and update it
    if env['session']['user']['_id'] == user['_id']:
        user_results = await call(
            'user/read_privileges',
            skip_events=[Event.PERM],
            env=env,
            query=[{'_id': user['_id']}],
        )
        env['session']['user'] = user_results['args']['docs'][0]

    return results


async def _delete_group(env: 'NawahEnv', query: 'Query') -> 'Results':
    # Confirm group is valid
    results = await call(
        'group/read',
        skip_events=[Event.PERM],
        env=env,
        query=[{'_id': query['group'][0]}],
    )
    if not results['args']['count']:
        raise FuncException(
            status=400, msg='Group is invalid.', args={'code': 'INVALID_GROUP'}
        )
    # Get user details
    results = await call(
        'user/read', skip_events=[Event.PERM], env=env, query=[{'_id': query['_id'][0]}]
    )
    if not results['args']['count']:
        raise FuncException(
            status=400, msg='User is invalid.', args={'code': 'INVALID_USER'}
        )
    user = results['args']['docs'][0]
    # Confirm group was not added before
    if query['group'][0] not in user['groups']:
        raise FuncException(
            status=400,
            msg='User is not a member of the group.',
            args={'code': 'GROUP_NOT_ADDED'},
        )
    # Update the user
    results = await call(
        'user/update',
        skip_events=[Event.PERM],
        env=env,
        query=[{'_id': query['_id'][0]}],
        doc={'groups': {'$del_val': [query['group'][0]]}},
    )
    # if update fails, return update results
    if results['status'] != 200:
        return results
    # Check if the updated User doc belongs to current session and update it
    if env['session']['user']['_id'] == user['_id']:
        user_results = await call(
            'user/read_privileges',
            skip_events=[Event.PERM],
            env=env,
            query=[{'_id': user['_id']}],
        )
        env['session']['user'] = user_results['args']['docs'][0]

    return results
