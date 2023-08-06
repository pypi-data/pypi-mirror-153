'''Provides 'session' Module Functions callables'''

import datetime
import secrets
from typing import TYPE_CHECKING, Optional

from passlib.hash import pbkdf2_sha512

from nawah.config import Config
from nawah.enums import Event
from nawah.exceptions import FuncException
from nawah.utils import call

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahDoc, NawahEnv, Results


async def _auth(
    env: 'NawahEnv', doc: 'NawahDoc', skip_status_check: Optional[None]
) -> 'Results':
    for attr in Config.modules['user'].unique_attrs:
        if attr in doc.keys():
            key = attr
            break
    user_query = [{key: doc[key], '$limit': 1}]
    if 'groups' in doc and doc['groups']:
        user_query.append(
            [{'groups': {'$in': doc['groups']}}, {'privileges': {'*': ['*']}}]
        )

    user_results = await call(
        'user/read',
        skip_events=[Event.PERM],
        env=env,
        query=user_query,
        args={'skip_sanitise_results': True},
    )
    if not user_results['args']['count'] or not pbkdf2_sha512.verify(
        doc['hash'],
        user_results['args']['docs'][0][f'{key}_hash'],
    ):
        raise FuncException(
            status=403,
            msg='Wrong auth credentials.',
            args={'code': 'INVALID_CREDS'},
        )

    user = user_results['args']['docs'][0]

    if skip_status_check is not True:
        if user['status'] in ['banned', 'deleted']:
            raise FuncException(
                status=403,
                msg=f'User is {user["status"]}.',
                args={'code': 'INVALID_USER'},
            )

        if user['status'] == 'disabled_password':
            raise FuncException(
                status=403,
                msg='User password is disabled.',
                args={'code': 'INVALID_USER'},
            )

    token = secrets.token_urlsafe(32)
    session = {
        'user': user['_id'],
        'groups': doc['groups'] if 'groups' in doc.keys() else [],
        'host_add': env['REMOTE_ADDR'],
        'user_agent': env['HTTP_USER_AGENT'],
        'expiry': (
            datetime.datetime.utcnow() + datetime.timedelta(days=30)
        ).isoformat(),
        'token_hash': pbkdf2_sha512.using(rounds=100000).hash(token),
    }

    results = await call(
        'session/create', skip_events=[Event.PERM], env=env, doc=session
    )
    if results['status'] != 200:
        return results

    session['_id'] = results['args']['docs'][0]['_id']
    session['user'] = user
    del session['token_hash']
    session['token'] = token
    results['args']['docs'][0] = session

    # read user privileges and return them
    user_results = await call(
        'user/read_privileges',
        skip_events=[Event.PERM],
        env=env,
        query=[{'_id': user['_id']}],
    )
    if user_results['status'] != 200:
        return user_results
    results['args']['docs'][0]['user'] = user_results['args']['docs'][0]

    # Create CONN_AUTH Analytic doc
    # if Config.analytics_events['session_conn_auth']:
    #     analytic_doc = {
    #         'event': 'CONN_AUTH',
    #         'subevent': env['client_app'],
    #         'args': {
    #             'user': user_results['args']['docs'][0]['_id'],
    #             'session': results['args']['docs'][0]['_id'],
    #             'REMOTE_ADDR': env['REMOTE_ADDR'],
    #             'HTTP_USER_AGENT': env['HTTP_USER_AGENT'],
    #         },
    #     }
    #     analytic_results = await Registry.module('analytic').create(
    #         skip_events=[Event.PERM], env=env, doc=analytic_doc
    #     )
    #     if analytic_results['status'] != 200:
    #         logger.error(
    #             f'Failed to create \'Analytic\' doc: {analytic_doc}. Results: {analytic_results}'
    #         )
    # Create USER_AUTH Analytic doc
    # if Config.analytics_events['session_user_auth']:
    #     analytic_doc = {
    #         'event': 'USER_AUTH',
    #         'subevent': user_results['args']['docs'][0]['_id'],
    #         'args': {
    #             'session': results['args']['docs'][0]['_id'],
    #             'REMOTE_ADDR': env['REMOTE_ADDR'],
    #             'HTTP_USER_AGENT': env['HTTP_USER_AGENT'],
    #             'client_app': env['client_app'],
    #         },
    #     }
    #     analytic_results = await Registry.module('analytic').create(
    #         skip_events=[Event.PERM], env=env, doc=analytic_doc
    #     )
    #     if analytic_results['status'] != 200:
    #         logger.error(
    #             f'Failed to create \'Analytic\' doc: {analytic_doc}. Results: {analytic_results}'
    #         )

    return {
        'status': 200,
        'msg': 'You were successfully authed.',
        'args': {'session': results['args']['docs'][0]},
    }


async def _reauth(env: 'NawahEnv', query: 'Query') -> 'Results':
    if str(query['_id'][0]) == 'f00000000000000000000012':
        raise FuncException(
            status=400,
            msg='Reauth is not required for \'__ANON\' user.',
            args={'code': 'ANON_REAUTH'},
        )

    session_query = [{'_id': query['_id'][0]}]
    if query['groups'][0]:
        session_query.append({'groups': {'$in': query['groups'][0]}})
    results = await call(
        'session/read', skip_events=[Event.PERM], env=env, query=session_query
    )
    if not results['args']['count']:
        raise FuncException(
            status=403, msg='Session is invalid.', args={'code': 'INVALID_SESSION'}
        )

    if not pbkdf2_sha512.verify(
        query['token'][0], results['args']['docs'][0]['token_hash']
    ):
        raise FuncException(
            status=403,
            msg='Reauth token hash invalid.',
            args={'code': 'INVALID_REAUTH_HASH'},
        )

    del results['args']['docs'][0]['token_hash']
    results['args']['docs'][0]['token'] = query['token'][0]

    if results['args']['docs'][0]['expiry'] < datetime.datetime.utcnow().isoformat():
        results = await call(
            'session/delete',
            skip_events=[Event.PERM, Event.SOFT],
            env=env,
            query=[{'_id': env['session']['_id']}],
        )
        raise FuncException(
            status=403, msg='Session had expired.', args={'code': 'SESSION_EXPIRED'}
        )

    # update user's last_login timestamp
    await call(
        'user/update',
        skip_events=[Event.PERM],
        env=env,
        query=[{'_id': results['args']['docs'][0]['user']}],
        doc={'login_time': datetime.datetime.utcnow().isoformat()},
    )
    await call(
        'session/update',
        skip_events=[Event.PERM],
        env=env,
        query=[{'_id': results['args']['docs'][0]['_id']}],
        doc={
            'expiry': (
                datetime.datetime.utcnow() + datetime.timedelta(days=30)
            ).isoformat()
        },
    )
    # read user privileges and return them
    user_results = await call(
        'user/read_privileges',
        skip_events=[Event.PERM],
        env=env,
        query=[{'_id': results['args']['docs'][0]['user']['_id']}],
    )
    results['args']['docs'][0]['user'] = user_results['args']['docs'][0]

    # Create CONN_AUTH Analytic doc
    # if Config.analytics_events['session_conn_reauth']:
    #     analytic_doc = {
    #         'event': 'CONN_REAUTH',
    #         'subevent': env['client_app'],
    #         'args': {
    #             'user': user_results['args']['docs'][0]['_id'],
    #             'session': results['args']['docs'][0]['_id'],
    #             'REMOTE_ADDR': env['REMOTE_ADDR'],
    #             'HTTP_USER_AGENT': env['HTTP_USER_AGENT'],
    #         },
    #     }
    #     analytic_results = await Registry.module('analytic').create(
    #         skip_events=[Event.PERM], env=env, doc=analytic_doc
    #     )
    #     if analytic_results['status'] != 200:
    #         logger.error(
    #             f'Failed to create \'Analytic\' doc: {analytic_doc}. Results: {analytic_results}'
    #         )
    # Create USER_AUTH Analytic doc
    # if Config.analytics_events['session_user_reauth']:
    #     analytic_doc = {
    #         'event': 'USER_REAUTH',
    #         'subevent': user_results['args']['docs'][0]['_id'],
    #         'args': {
    #             'session': results['args']['docs'][0]['_id'],
    #             'REMOTE_ADDR': env['REMOTE_ADDR'],
    #             'HTTP_USER_AGENT': env['HTTP_USER_AGENT'],
    #             'client_app': env['client_app'],
    #         },
    #     }
    #     analytic_results = await Registry.module('analytic').create(
    #         skip_events=[Event.PERM], env=env, doc=analytic_doc
    #     )
    #     if analytic_results['status'] != 200:
    #         logger.error(
    #             f'Failed to create \'Analytic\' doc: {analytic_doc}. Results: {analytic_results}'
    #         )

    return {
        'status': 200,
        'msg': 'You were successfully reauthed.',
        'args': {'session': results['args']['docs'][0]},
    }


async def _signout(env: 'NawahEnv', query: 'Query') -> 'Results':
    if str(query['_id'][0]) == 'f00000000000000000000012':
        raise FuncException(
            status=400,
            msg='Singout is not allowed for \'__ANON\' user.',
            args={'code': 'ANON_SIGNOUT'},
        )

    results = await call(
        'session/read',
        skip_events=[Event.PERM],
        env=env,
        query=[{'_id': query['_id'][0]}],
    )

    if not results['args']['count']:
        raise FuncException(
            status=403, msg='Session is invalid.', args={'code': 'INVALID_SESSION'}
        )

    results = await call(
        'session/delete',
        skip_events=[Event.PERM],
        env=env,
        query=[{'_id': env['session']['_id']}],
    )

    # Create CONN_AUTH Analytic doc
    # if Config.analytics_events['session_conn_deauth']:
    #     analytic_doc = {
    #         'event': 'CONN_DEAUTH',
    #         'subevent': env['client_app'],
    #         'args': {
    #             'user': env['session']['user']['_id'],
    #             'session': env['session']['_id'],
    #             'REMOTE_ADDR': env['REMOTE_ADDR'],
    #             'HTTP_USER_AGENT': env['HTTP_USER_AGENT'],
    #         },
    #     }
    #     analytic_results = await Registry.module('analytic').create(
    #         skip_events=[Event.PERM], env=env, doc=analytic_doc
    #     )
    #     if analytic_results['status'] != 200:
    #         logger.error(
    #             f'Failed to create \'Analytic\' doc: {analytic_doc}. Results: {analytic_results}'
    #         )
    # Create USER_AUTH Analytic doc
    # if Config.analytics_events['session_user_deauth']:
    #     analytic_doc = {
    #         'event': 'USER_DEAUTH',
    #         'subevent': env['session']['user']['_id'],
    #         'args': {
    #             'session': env['session']['_id'],
    #             'REMOTE_ADDR': env['REMOTE_ADDR'],
    #             'HTTP_USER_AGENT': env['HTTP_USER_AGENT'],
    #             'client_app': env['client_app'],
    #         },
    #     }
    #     analytic_results = await Registry.module('analytic').create(
    #         skip_events=[Event.PERM], env=env, doc=analytic_doc
    #     )
    #     if analytic_results['status'] != 200:
    #         logger.error(
    #             f'Failed to create \'Analytic\' doc: {analytic_doc}. Results: {analytic_results}'
    #         )

    return {
        'status': 200,
        'msg': 'You are successfully signed-out.',
        'args': {'session': {'_id': 'f00000000000000000000012'}},
    }
