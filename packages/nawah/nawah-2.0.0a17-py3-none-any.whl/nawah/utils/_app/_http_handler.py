import datetime
import json
import logging
import re
from typing import TYPE_CHECKING, MutableMapping, MutableSequence, cast

import aiohttp.web
from multidict import MultiDict
from passlib.hash import pbkdf2_sha512
from requests_toolbelt.multipart import decoder

from nawah import data as Data
from nawah.classes import app_encoder
from nawah.config import Config
from nawah.enums import Event
from nawah.exceptions import InvalidAttrException

from .._call import call
from .._config import _compile_anon_session, _compile_anon_user
from .._validate import validate_doc

if TYPE_CHECKING:
    from nawah.classes import Attr
    from nawah.types import NawahDoc, NawahEnv

logger = logging.getLogger('nawah')


async def _http_handler(request: aiohttp.web.Request):
    headers = MultiDict(
        [
            ('Server', 'Nawah'),
            ('Powered-By', 'Nawah, https://nawah.masaar.com'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET,POST,OPTIONS'),
            (
                'Access-Control-Allow-Headers',
                'Content-Type,X-Auth-Bearer,X-Auth-Token,X-Auth-App',
            ),
            ('Access-Control-Expose-Headers', 'Content-Disposition'),
        ]
    )

    logger.debug('Received new %s request: %s', request.method, request.match_info)

    if request.method == 'OPTIONS':
        return aiohttp.web.Response(
            status=200,
            headers=headers,
            body=app_encoder.encode(
                {
                    'status': 200,
                    'msg': 'OPTIONS request is allowed',
                }
            ),
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
        ).seconds > 259:
            Config.sys.ip_quota[str(request.remote)][
                'last_check'
            ] = datetime.datetime.utcnow()
            Config.sys.ip_quota[str(request.remote)]['counter'] = Config.quota_ip_min
        else:
            if Config.sys.ip_quota[str(request.remote)]['counter'] - 1 <= 0:
                logger.warning(
                    'Denying \'%s\' request from \'%s\' for hitting IP quota',
                    request.method,
                    request.remote,
                )
                headers['Content-Type'] = 'application/json; charset=utf-8'
                return aiohttp.web.Response(
                    status=429,
                    headers=headers,
                    body=app_encoder.encode(
                        {
                            'status': 429,
                            'msg': 'You have hit calls quota from this IP',
                            'args': {'code': 'CORE_REQ_IP_QUOTA_HIT'},
                        }
                    ),
                )

            Config.sys.ip_quota[str(request.remote)]['counter'] -= 1

    module_name = request.url.parts[1]
    func_name = request.url.parts[2]
    request_args = dict(request.match_info.items())

    # Extract Args Sets based on request.method
    args_sets = Config.modules[module_name].funcs[func_name].query_attrs
    args_sets = cast(MutableSequence[MutableMapping[str, 'Attr']], args_sets)

    # Attempt to validate query as doc
    for args_set in args_sets or []:
        if len(args_set.keys()) == len(args_set.keys()) and sum(
            1 for arg in args_set.keys() if arg in args_set.keys()
        ) == len(args_set.keys()):
            # Check presence and validate all attrs in doc args
            try:
                exception: Exception
                validate_doc(mode='create', doc=request_args, attrs=args_set)  # type: ignore
            except InvalidAttrException as e:
                exception = e
                headers['Content-Type'] = 'application/json; charset=utf-8'
                return aiohttp.web.Response(
                    status=400,
                    headers=headers,
                    body=app_encoder.encode(
                        {
                            'status': 400,
                            'msg': f'{str(e)} for \'{request.method}\' request on module '
                            '\'{module_name}\'',
                            'args': {'code': f'{module_name.upper()}_INVALID_ATTR'},
                        }
                    ).encode('utf-8'),
                )
            break

    conn = Data.create_conn()
    env: 'NawahEnv' = {
        'conn': conn,
        'REMOTE_ADDR': request.remote or 'localhost',
        'client_app': '__public',
        'args': {},
    }

    try:
        env['HTTP_USER_AGENT'] = request.headers['user-agent']
        env['HTTP_ORIGIN'] = request.headers['origin']
    except:
        env['HTTP_USER_AGENT'] = ''
        env['HTTP_ORIGIN'] = ''

    if 'X-Auth-Bearer' in request.headers or 'X-Auth-Token' in request.headers:
        logger.debug('Detected \'X-Auth\' header[s]')
        if (
            'X-Auth-Bearer' not in request.headers
            or 'X-Auth-Token' not in request.headers
            or 'X-Auth-App' not in request.headers
        ):
            logger.debug('Denying request due to missing \'X-Auth\' header')
            headers['Content-Type'] = 'application/json; charset=utf-8'
            return aiohttp.web.Response(
                status=400,
                headers=headers,
                body=app_encoder.encode(
                    {
                        'status': 400,
                        'msg': 'One \'X-Auth\' headers was set but not the other',
                    }
                ).encode('utf-8'),
            )
        # [TODO] Add condition to now allow a connection from a client with client_app = __sys
        if Config.client_apps and (
            request.headers['X-Auth-App'] not in Config.client_apps
            or (
                Config.client_apps[request.headers['X-Auth-App']].type == 'web'
                and env['HTTP_ORIGIN']
                not in Config.client_apps[request.headers['X-Auth-App']].origin
            )
        ):
            logger.debug('Denying request due to unauthorised client_app')
            headers['Content-Type'] = 'application/json; charset=utf-8'
            return aiohttp.web.Response(
                status=403,
                headers=headers,
                body=app_encoder.encode(
                    {
                        'status': 403,
                        'msg': 'X-Auth headers could not be verified',
                        'args': {'code': 'CORE_SESSION_INVALID_XAUTH'},
                    }
                ).encode('utf-8'),
            )
        try:
            session_results = await call(
                'session/read',
                skip_events=[Event.PERM],
                env=env,
                query=[
                    {
                        '_id': request.headers['X-Auth-Bearer'],
                    }
                ],
            )
        except:
            headers['Content-Type'] = 'application/json; charset=utf-8'
            if Config.debug:
                return aiohttp.web.Response(
                    status=500,
                    headers=headers,
                    body=app_encoder.encode(
                        {
                            'status': 500,
                            'msg': f'Unexpected error has occurred [{str(exception)}]',
                            'args': {
                                'code': 'CORE_SERVER_ERROR',
                                'err': str(exception),
                            },
                        }
                    ).encode('utf-8'),
                )

            return aiohttp.web.Response(
                status=500,
                headers=headers,
                body=app_encoder.encode(
                    {
                        'status': 500,
                        'msg': 'Unexpected error has occurred',
                        'args': {'code': 'CORE_SERVER_ERROR'},
                    }
                ).encode('utf-8'),
            )

        if not session_results['args']['count'] or not pbkdf2_sha512.verify(
            request.headers['X-Auth-Token'],
            session_results['args']['docs'][0]['token_hash'],
        ):
            logger.debug('Denying request due to missing failed Call Authorisation')
            headers['Content-Type'] = 'application/json; charset=utf-8'
            return aiohttp.web.Response(
                status=403,
                headers=headers,
                body=app_encoder.encode(
                    {
                        'status': 403,
                        'msg': 'X-Auth headers could not be verified',
                        'args': {'code': 'CORE_SESSION_INVALID_XAUTH'},
                    }
                ).encode('utf-8'),
            )
        session = session_results['args']['docs'][0]
        session_results = await call(
            'session/reauth',
            skip_events=[Event.PERM],
            env=env,
            query=[
                {
                    '_id': request.headers['X-Auth-Bearer'],
                    'token': request.headers['X-Auth-Token'],
                    'groups': [],
                }
            ],
        )
        logger.debug('Denying request due to fail to reauth')
        if session_results['status'] != 200:
            headers['Content-Type'] = 'application/json; charset=utf-8'
            return aiohttp.web.Response(
                status=403,
                headers=headers,
                body=app_encoder.encode(session_results).encode('utf-8'),
            )

        session = session_results['args']['session']
    else:
        anon_user = _compile_anon_user()
        anon_session = _compile_anon_session()
        anon_session['user'] = anon_user
        session = anon_session

    env['session'] = json.loads(app_encoder.encode(session))

    doc: 'NawahDoc' = {}

    if 'Content-Type' in request.headers:
        doc_content = await request.content.read()
        # Check Content-Type to decide how to deserialise content
        if request.headers['Content-Type'].startswith('multipart/form-data;'):
            multipart_content_type = request.headers['Content-Type']
            doc = {}
            for part in decoder.MultipartDecoder(
                doc_content, multipart_content_type
            ).parts:
                content_disposition = part.headers[b'Content-Disposition'].decode(
                    'UTF-8'
                )
                attr_name_match = re.findall('name="([^"]+)"', content_disposition)
                if not attr_name_match:
                    continue
                attr_name = attr_name_match[0]
                doc[attr_name] = part.content
                # For non-file values, decode unto str
                if 'filename' not in content_disposition:
                    doc[attr_name] = doc[attr_name].decode('UTF-8')
        elif request.headers['Content-Type'].startswith('application/json;'):
            doc = json.loads(doc_content)

    results = await call(
        f'{module_name}/{func_name}', env=env, query=[request_args], doc=doc
    )

    logger.debug('Closing connection')
    env['conn'].close()

    if 'return' not in results['args'] or results['args']['return'] == 'json':
        if 'return' in results['args']:
            del results['args']['return']
        headers['Content-Type'] = 'application/json; charset=utf-8'
        if results['status'] == 404:
            return aiohttp.web.Response(
                status=results['status'],
                headers=headers,
                body=app_encoder.encode(
                    {'status': 404, 'msg': 'Requested content not found'}
                ).encode('utf-8'),
            )
        return aiohttp.web.Response(
            status=results['status'],
            headers=headers,
            body=app_encoder.encode(results),
        )

    if results['args']['return'] == 'file':
        del results['args']['return']
        status = results['status']
        expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        headers['Last-Modified'] = str(results['args']['docs'][0]['lastModified'])
        headers['Content-Type'] = results['args']['docs'][0]['type']
        headers['Cache-Control'] = 'public, max-age=31536000'
        headers['Expires'] = expiry_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
        content = results['args']['docs'][0]['content']
        if 'If-Modified-Since' in request.headers:
            if request.headers['If-Modified-Since'] == headers['Last-Modified']:
                status = 304
                content = b''
        return aiohttp.web.Response(
            status=status,
            headers=headers,
            body=content,
        )

    if results['args']['return'] == 'msg':
        del results['args']['return']
        headers['Content-Type'] = 'application/json; charset=utf-8'
        return aiohttp.web.Response(
            status=results['status'], headers=headers, body=results['msg']
        )

    headers['Content-Type'] = 'application/json; charset=utf-8'
    return aiohttp.web.Response(
        status=405,
        headers=headers,
        body=app_encoder.encode({'status': 405, 'msg': 'METHOD NOT ALLOWED'}),
    )
