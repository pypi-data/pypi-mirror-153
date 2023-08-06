'''Provides '''

import datetime
from typing import TYPE_CHECKING, Literal, MutableMapping, MutableSequence

from bson import ObjectId

from nawah.config import Config

if TYPE_CHECKING:
    from nawah.types import NawahEnv, NawahSession, Results, ResultsArgs


def mock_results(
    *, status: int, msg: str = None, args: 'ResultsArgs' = None
) -> 'Results':
    '''Returns dict structured as call results'''

    return {
        'status': status,
        'msg': msg or 'Mock results',
        'args': args or {},
    }


def mock_env(*, session: 'NawahSession' = None) -> 'NawahEnv':
    '''Returns dict structured as 'Env' dict. If no value provided for 'session', value would be
    return of 'mock_session()' '''

    return {
        'client_app': '__test',
        'session': session or mock_session(),
        'args': {},
    }


def mock_session(
    *, user: MutableMapping = None, groups: MutableSequence[str] = None
) -> 'NawahSession':
    '''Returns dict structured as 'session' of 'Env' dict. If no value provided for 'user', value
    would be return of 'mock_user()'. If no value provided for 'groups', value would be empty
    list'''

    return {
        'user': user or {},
        'groups': groups or [],
        'host_add': '127.0.0.1',
        'user_agent': 'Nawah Framework Testing Tools',
        'expiry': datetime.datetime.utcnow().isoformat(),
        'token_hash': '__token',
        'create_time': datetime.datetime.utcnow().isoformat(),
    }


def mock_user(  # pylint: disable=too-many-arguments
    *,
    _id: ObjectId = None,
    name: MutableMapping[str, str] = None,
    locale: str = None,
    create_time: str = None,
    login_time: str = None,
    groups: MutableSequence[str] = None,
    privileges: MutableMapping[str, MutableSequence[str]] = None,
    status: Literal['active', 'banned', 'deleted', 'disabled_password'] = None,
    **kwargs
) -> MutableMapping:
    '''Thin wrapper for 'mock_doc'. Returns dict structured as 'user' doc'''

    return mock_doc(
        _id=_id,
        name=name or {locale: '__name' for locale in Config.locales},
        locale=locale or Config.locale,
        create_time=create_time or datetime.datetime.utcnow().isoformat(),
        login_time=login_time or datetime.datetime.utcnow().isoformat(),
        groups=groups or ['f00000000000000000000013'],
        privileges=privileges or {},
        status=status,
        **kwargs,
    )


def mock_doc(_id: ObjectId = None, **kwargs):
    '''Returns dict structured as doc'''

    return {
        '_id': _id or ObjectId(),
        **kwargs,
    }
