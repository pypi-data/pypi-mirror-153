import aiohttp.web
from multidict import MultiDict

from nawah.classes import app_encoder
from nawah.config import Config


async def _not_found_handler(_):
    headers = MultiDict(
        [
            ('Server', 'Nawah'),
            ('Powered-By', 'Nawah, https://nawah.masaar.com'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET,POST'),
            ('Access-Control-Allow-Headers', 'Content-Type'),
            ('Access-Control-Expose-Headers', 'Content-Disposition'),
        ]
    )
    return aiohttp.web.Response(
        status=404,
        headers=headers,
        body=app_encoder.encode({'status': 404, 'msg': '404 NOT FOUND'}),
    )


async def _not_allowed_handler(_):
    headers = MultiDict(
        [
            ('Server', 'Nawah'),
            ('Powered-By', 'Nawah, https://nawah.masaar.com'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', '*'),
            ('Access-Control-Allow-Headers', 'Content-Type'),
            ('Access-Control-Expose-Headers', 'Content-Disposition'),
        ]
    )
    return aiohttp.web.Response(
        status=405,
        headers=headers,
        body=app_encoder.encode({'status': 405, 'msg': '404 NOT ALLOWED'}),
    )


async def _root_handler(_):
    headers = MultiDict(
        [
            ('Server', 'Nawah'),
            ('Powered-By', 'Nawah, https://nawah.masaar.com'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET'),
            ('Access-Control-Allow-Headers', 'Content-Type'),
            ('Access-Control-Expose-Headers', 'Content-Disposition'),
        ]
    )
    return aiohttp.web.Response(
        status=200,
        headers=headers,
        body=app_encoder.encode(
            {
                'status': 200,
                'msg': f'Welcome to {Config.sys.name}!',
                'args': {'version': Config.sys.version, 'powered_by': 'Nawah'},
            }
        ),
    )
