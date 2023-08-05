'''Provides 'user' Module Functions callables'''

import copy
from typing import TYPE_CHECKING, Optional

from bson import ObjectId

from nawah.config import Config
from nawah.enums import Event, NawahValues
from nawah.exceptions import FuncException, InvalidAttrException
from nawah.utils import call, encode_attr_type, validate_attr

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahDoc, NawahEnv, NawahEvents, Results


async def _read(
    skip_events: 'NawahEvents',
    env: 'NawahEnv',
    query: 'Query',
    skip_user_settings: Optional[bool],
) -> 'Results':
    skip_events.append(Event.PERM)
    read_results = await call(
        'base/read', module_name='user', skip_events=skip_events, env=env, query=query
    )

    if read_results['status'] != 200:
        return read_results

    if skip_user_settings is True:
        return read_results

    for i, _ in enumerate(read_results['args']['docs']):
        user = read_results['args']['docs'][i]
        for auth_attr in Config.user_attrs:
            del user[f'{auth_attr}_hash']
        if Config.user_doc_settings:
            setting_results = await call(
                'base/read',
                module_name='setting',
                skip_events=[Event.PERM],
                env=env,
                query=[{'user': user['_id'], 'var': {'$in': Config.user_doc_settings}}],
            )
            user_doc_settings = copy.copy(Config.user_doc_settings)
            if setting_results['args']['count']:
                for setting_doc in setting_results['args']['docs']:
                    user_doc_settings.remove(setting_doc['var'])
                    user[setting_doc['var']] = setting_doc['val']
            # Forward-compatibility: If user was created before presence
            # of any user_doc_settings, add them with default value
            for setting_attr in user_doc_settings:
                user[setting_attr] = Config.user_settings[setting_attr].default
                # Set NawahValues.NONE_VALUE to None if it was default
                if user[setting_attr] == NawahValues.NONE_VALUE:
                    user[setting_attr] = None

    return read_results


async def _create(
    skip_events: 'NawahEvents', env: 'NawahEnv', doc: 'NawahDoc'
) -> 'Results':
    if Event.ATTRS_DOC not in skip_events:
        doc['groups'] = [ObjectId('f00000000000000000000013')]
    user_settings = {}
    for setting_name, setting in Config.user_settings.items():
        if setting.type == 'user_sys':
            user_settings[setting_name] = copy.deepcopy(setting.default)
        else:
            if setting_name in doc:
                try:
                    validate_attr(
                        mode='create',
                        attr_name=setting_name,
                        attr_type=setting.val_type,
                        attr_val=doc[setting_name],
                    )
                    user_settings[setting_name] = doc[setting_name]
                except InvalidAttrException as validation_exception:
                    raise FuncException(
                        status=400,
                        msg=f'Invalid settings attr \'{setting_name}\' for \'create\' request on '
                        'module \'user\'',
                        args={'code': 'CREATE_INVALID_SETTING'},
                    ) from validation_exception

            if setting.default == NawahValues.NONE_VALUE:
                raise FuncException(
                    status=400,
                    msg=f'Missing settings attr \'{setting_name}\' for \'create\' request on '
                    'module \'user\'',
                    args={'code': 'MISSING_ATTR'},
                )

            user_settings[setting_name] = copy.deepcopy(setting.default)

    create_results = await call(
        'base/create', skip_events=[Event.PERM], module_name='user', env=env, doc=doc
    )

    for setting_name, setting_val in user_settings.items():
        setting_results = await call(
            'setting/create',
            skip_events=[Event.PERM, Event.ATTRS_DOC],
            env=env,
            doc={
                'user': create_results['args']['docs'][0]['_id'],
                'var': setting_name,
                'val_type': encode_attr_type(
                    attr_type=Config.user_settings[setting_name].val_type
                ),
                'val': setting_val,
                'type': Config.user_settings[setting_name].type,
            },
        )
        if setting_results['status'] != 200:
            return setting_results

    return create_results


async def _read_privileges(env: 'NawahEnv', query: 'Query') -> 'Results':
    # Confirm _id is valid
    results = await call(
        'user/read',
        skip_events=[Event.PERM],
        env=env,
        query=[{'_id': query['_id'][0]}],
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
