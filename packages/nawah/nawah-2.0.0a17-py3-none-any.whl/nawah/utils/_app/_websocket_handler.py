import asyncio
import datetime
import json
import logging
import random
import traceback
from functools import partial
from typing import TYPE_CHECKING

import aiohttp.web

from nawah import data as Data
from nawah.classes import app_encoder
from nawah.config import Config

from .._call import call
from .._config import _compile_anon_session, _compile_anon_user
from .._val import camel_to_upper
from ._utils import _close_session

if TYPE_CHECKING:
    from asyncio.futures import Future

    from nawah.types import NawahEnv

logger = logging.getLogger('nawah')


async def _websocket_handler(request: aiohttp.web.Request):
    conn = Data.create_conn()
    logger.debug('Websocket connection starting with client at \'%s\'', request.remote)
    ws = aiohttp.web.WebSocketResponse()
    await ws.prepare(request)

    session_lock_key = random.random()

    while Config.sys.session_lock != session_lock_key:
        if Config.sys.session_lock is None:
            Config.sys.session_lock = session_lock_key

    Config.sys.session_counter += 1

    env: 'NawahEnv' = {
        'id': str(Config.sys.session_counter),
        'conn': conn,
        'REMOTE_ADDR': request.remote or 'localhost',
        'ws': ws,
        'init': False,
        'last_call': datetime.datetime.utcnow(),
        'quota': {
            'counter': Config.quota_anon_min,
            'last_check': datetime.datetime.utcnow(),
        },
        'args': {},
    }
    Config.sys.sessions[str(Config.sys.session_counter)] = env
    Config.sys.session_lock = None

    try:
        env['HTTP_USER_AGENT'] = request.headers['user-agent']
        env['HTTP_ORIGIN'] = request.headers['origin']
    except:
        env['HTTP_USER_AGENT'] = ''
        env['HTTP_ORIGIN'] = ''

    logger.debug(
        'Websocket connection #\'%s\' ready with client at \'%s\'',
        env['id'],
        env['REMOTE_ADDR'],
    )

    await ws.send_str(
        app_encoder.encode(
            {
                'status': 200,
                'msg': 'Connection ready',
                'args': {'code': 'CORE_CONN_READY'},
            }
        )
    )

    async for msg in ws:
        if 'conn' not in env:
            await ws.close()
            break
        logger.debug(
            'Received new message from session #\'%s\': %s', env['id'], msg.data[:256]
        )
        if msg.type == aiohttp.WSMsgType.TEXT:
            logger.debug(
                'Config.sys.ip_quota on session #\'%s\': %s',
                env['id'],
                Config.sys.ip_quota,
            )
            logger.debug(
                'session_quota: on session #\'%s\': %s', env['id'], env['quota']
            )
            # Check for IP quota
            if str(request.remote) not in Config.sys.ip_quota:
                Config.sys.ip_quota[str(request.remote)] = {
                    'counter': Config.quota_ip_min,
                    'last_check': datetime.datetime.utcnow(),
                }
            else:
                if (
                    datetime.datetime.utcnow()
                    - Config.sys.ip_quota[str(request.remote)]['last_check']
                ).seconds > 59:
                    Config.sys.ip_quota[str(request.remote)][
                        'last_check'
                    ] = datetime.datetime.utcnow()
                    Config.sys.ip_quota[str(request.remote)][
                        'counter'
                    ] = Config.quota_ip_min
                else:
                    # If hit quota, deny call
                    if Config.sys.ip_quota[str(request.remote)]['counter'] - 1 <= 0:
                        logger.warning(
                            'Denying Websocket request from \'%s\' for hitting IP quota',
                            request.remote,
                        )
                        asyncio.create_task(
                            _handle_msg(
                                env=env,
                                msg=msg,
                                decline_quota='ip',
                            )
                        )
                        continue
                    # Else, update quota counter
                    Config.sys.ip_quota[str(request.remote)]['counter'] -= 1
            # Check for session quota
            if (datetime.datetime.utcnow() - env['quota']['last_check']).seconds > 59:
                env['quota']['last_check'] = datetime.datetime.utcnow()
                env['quota']['counter'] = (
                    (Config.quota_anon_min - 1)
                    if not env['session']
                    or env['session']['token'] == Config.anon_token
                    else (Config.quota_auth_min - 1)
                )
                asyncio.create_task(_handle_msg(env=env, msg=msg))
            else:
                # If hit quota, deny call
                if env['quota']['counter'] - 1 <= 0:
                    asyncio.create_task(
                        _handle_msg(
                            env=env,
                            msg=msg,
                            decline_quota='session',
                        )
                    )
                    continue
                # Else, update quota counter
                env['quota']['counter'] -= 1
                asyncio.create_task(_handle_msg(env=env, msg=msg))

    if 'id' in env:
        await _close_session(env['id'])

    return ws


async def _handle_msg(
    env: 'NawahEnv',
    msg: aiohttp.WSMessage,
    decline_quota: str = None,
):
    try:
        env['last_call'] = datetime.datetime.utcnow()
        try:
            env['session']['token']
        except Exception:
            anon_user = _compile_anon_user()
            anon_session = _compile_anon_session()
            anon_session['user'] = anon_user
            env['session'] = json.loads(app_encoder.encode(anon_session))
        res = json.loads(msg.data)

        # Check if msg should be denied for quota hit
        if decline_quota == 'ip':
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 429,
                        'msg': 'You have hit calls quota from this IP',
                        'args': {
                            'call_id': res['call_id']
                            if 'call_id' in res.keys()
                            else None,
                            'code': 'CORE_REQ_IP_QUOTA_HIT',
                        },
                    }
                )
            )
            return

        if decline_quota == 'session':
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 429,
                        'msg': 'You have hit calls quota',
                        'args': {
                            'call_id': res['call_id']
                            if 'call_id' in res.keys()
                            else None,
                            'code': 'CORE_REQ_SESSION_QUOTA_HIT',
                        },
                    }
                )
            )
            return

        logger.debug('Decoded request: %s', app_encoder.encode(res))

        if 'endpoint' not in res.keys():
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 400,
                        'msg': 'Request missing endpoint',
                        'args': {
                            'call_id': res['call_id']
                            if 'call_id' in res.keys()
                            else None,
                            'code': 'CORE_REQ_NO_ENDPOINT',
                        },
                    }
                )
            )
            return

        if env['init'] is False:
            if res['endpoint'] != 'conn/verify':
                await env['ws'].send_str(
                    app_encoder.encode(
                        {
                            'status': 1008,
                            'msg': 'Request token is not accepted',
                            'args': {
                                'call_id': res['call_id']
                                if 'call_id' in res.keys()
                                else None,
                                'code': 'CORE_REQ_NO_VERIFY',
                            },
                        }
                    )
                )
                await env['ws'].close()
                return

            # [TODO] Add condition to now allow a connection from a client with client_app = __sys
            if Config.client_apps and (
                'doc' not in res
                or 'app' not in res['doc']
                or res['doc']['app'] not in Config.client_apps
                or (
                    Config.client_apps[res['doc']['app']].type == 'web'
                    and env['HTTP_ORIGIN']
                    not in Config.client_apps[res['doc']['app']].origin
                )
            ):
                await env['ws'].send_str(
                    app_encoder.encode(
                        {
                            'status': 1008,
                            'msg': 'Request token is not accepted',
                            'args': {
                                'call_id': res['call_id']
                                if 'call_id' in res.keys()
                                else None,
                                'code': 'CORE_REQ_NO_VERIFY',
                            },
                        }
                    )
                )
                await env['ws'].close()
                return

            env['init'] = True
            # [TODO] Add condition to now allow a connection from a client with client_app = __sys
            if not Config.client_apps:
                env['client_app'] = '__public'
            else:
                env['client_app'] = res['doc']['app']
            logger.debug('Connection on session #\'%s\' is verified', env['id'])
            # if Config.analytics_events['app_conn_verified']:
            #     asyncio.create_task(
            #         call(
            #             'analytic/create',
            #             skip_events=[Event.PERM],
            #             env=env,
            #             doc={
            #                 'event': 'CONN_VERIFIED',
            #                 'subevent': env['client_app'],
            #                 'args': {
            #                     'REMOTE_ADDR': env['REMOTE_ADDR'],
            #                     'HTTP_USER_AGENT': env['HTTP_USER_AGENT'],
            #                 },
            #             },
            #         )
            #     )
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 200,
                        'msg': 'Connection established',
                        'args': {
                            'call_id': res['call_id']
                            if 'call_id' in res.keys()
                            else None,
                            'code': 'CORE_CONN_OK',
                        },
                    }
                )
            )
            return

        if res['endpoint'] == 'conn/close':
            logger.debug(
                f'Received connection close instructions on session #\'{env["id"]}\''
            )
            await env['ws'].close()
            return

        if res['endpoint'] == 'heart/beat':
            logger.debug(f'Received connection heartbeat on session #\'{env["id"]}\'')
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 200,
                        'msg': 'Heartbeat received',
                        'args': {
                            'call_id': res['call_id']
                            if 'call_id' in res.keys()
                            else None,
                            'code': 'CORE_HEARTBEAT_OK',
                        },
                    }
                )
            )
            return

        res['endpoint'] = res['endpoint']

        if (
            res['endpoint'] in ['session/auth', 'session/reauth']
            and str(env['session']['_id']) != 'f00000000000000000000012'
        ):
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 400,
                        'msg': 'You are already authed',
                        'args': {
                            'call_id': res['call_id']
                            if 'call_id' in res.keys()
                            else None,
                            'code': 'CORE_SESSION_ALREADY_AUTHED',
                        },
                    }
                )
            )
            return

        if (
            res['endpoint'] == 'session/signout'
            and str(env['session']['_id']) == 'f00000000000000000000012'
        ):
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 400,
                        'msg': 'Singout is not allowed for \'__ANON\' user',
                        'args': {
                            'call_id': res['call_id']
                            if 'call_id' in res.keys()
                            else None,
                            'code': 'CORE_SESSION_ANON_SIGNOUT',
                        },
                    }
                )
            )
            return

        if 'query' not in res.keys():
            res['query'] = []
        if 'doc' not in res.keys():
            res['doc'] = {}
        if 'call_id' not in res.keys():
            res['call_id'] = ''

        request = {
            'call_id': res['call_id'],
            # 'sid': res['sid'] or False,
            'query': res['query'],
            'doc': res['doc'],
            'path': res['endpoint'].split('/'),
        }

        if len(request['path']) != 2:
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 400,
                        'msg': 'Endpoint path is invalid',
                        'args': {
                            'call_id': request['call_id'],
                            'code': 'CORE_REQ_INVALID_PATH',
                        },
                    }
                )
            )
            return

        module = request['path'][0]

        if module not in Config.modules:
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 400,
                        'msg': 'Endpoint module is invalid',
                        'args': {
                            'call_id': request['call_id'],
                            'code': 'CORE_REQ_INVALID_MODULE',
                        },
                    }
                )
            )
            return

        if request['path'][1] not in Config.modules[module].funcs:
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 400,
                        'msg': 'Endpoint is invalid',
                        'args': {
                            'call_id': request['call_id'],
                            'code': 'CORE_REQ_INVALID_METHOD',
                        },
                    }
                )
            )
            return

        if Config.modules[module].funcs[request['path'][1]].get_func:
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 400,
                        'msg': 'Endpoint is a GET Function',
                        'args': {
                            'call_id': request['call_id'],
                            'code': 'CORE_REQ_GET_FUNC',
                        },
                    }
                )
            )
            return

        # if not request['sid']:
        request['sid'] = 'f00000000000000000000012'

        query = request['query']
        doc = request['doc']
        # await _process_file_obj(doc=doc, env=env)
        call_task = asyncio.create_task(
            call(
                f'{module}/{request["path"][1]}',
                skip_events=[],
                env=env,
                query=query,
                doc=doc,
            )
        )
        call_task.add_done_callback(
            partial(_call_callback, env=env, call_id=request['call_id'])
        )

    except Exception as e:
        logger.error(f'An error occurred. Details: {traceback.format_exc()}')
        if Config.debug:
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 500,
                        'msg': f'Unexpected error has occurred [{str(e)}]',
                        'args': {
                            'code': 'CORE_SERVER_ERROR',
                            'err': str(e),
                            'call_id': request['call_id'],
                        },
                    }
                )
            )
        else:
            await env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': 500,
                        'msg': 'Unexpected error has occurred',
                        'args': {
                            'code': 'CORE_SERVER_ERROR',
                            'call_id': request['call_id'],
                        },
                    }
                )
            )


def _call_callback(call_task: 'Future', env: 'NawahEnv', call_id: str):
    try:
        results = call_task.result()
        results['args']['call_id'] = call_id
        asyncio.create_task(env['ws'].send_str(app_encoder.encode(results)))
    except Exception as e:
        status = getattr(e, 'status', 500)
        msg = 'Unexpected error has occurred'
        code = camel_to_upper(e.__class__.__name__)
        if e.args:
            msg = e.args[0]
            if len(e.args) == 2:
                if isinstance(e.args[1], dict):
                    if 'args' in e.args[1]:
                        if 'code' in e.args[1]['args']:
                            code = e.args[1]['args']['code']
                    if 'status' in e.args[1]:
                        status = e.args[1]['status']

        asyncio.create_task(
            env['ws'].send_str(
                app_encoder.encode(
                    {
                        'status': status,
                        'msg': msg,
                        'args': {'code': code, 'call_id': call_id},
                    }
                )
            )
        )
