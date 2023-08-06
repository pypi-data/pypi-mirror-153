'''Provides types used in Nawah'''

from typing import (TYPE_CHECKING, Any, Literal, MutableMapping,
                    MutableSequence, TypedDict, Union)

from nawah.enums import Event

if TYPE_CHECKING:
    from datetime import datetime

    from aiohttp.web import WebSocketResponse
    from motor.motor_asyncio import AsyncIOMotorClient

    from nawah.classes import Package


class Results(TypedDict):
    '''Provides type-hint for return of Nawah Function'''

    status: int
    msg: str
    args: 'ResultsArgs'


ResultsArgs = MutableMapping[str, Any]


class AppPackage(TypedDict):
    '''Provides type-hint for item of 'Config.packages' '''

    package: 'Package'
    modules: MutableSequence[str]


class AnalyticsEvents(TypedDict):
    '''Provides type-hint for 'analytics_events' App Config Attr'''

    app_conn_verified: bool
    session_conn_auth: bool
    session_user_auth: bool
    session_conn_reauth: bool
    session_user_reauth: bool
    session_conn_deauth: bool
    session_user_deauth: bool


class IPQuota(TypedDict):
    '''Provides type-hint for dict used to track IP user quota'''

    counter: int
    last_check: 'datetime'


NawahEvents = MutableSequence[Event]


class NawahEnv(TypedDict, total=False):
    '''Provides type-hint for 'Env' dict'''

    id: str
    init: bool
    conn: 'AsyncIOMotorClient'
    REMOTE_ADDR: str
    HTTP_USER_AGENT: str
    HTTP_ORIGIN: str
    client_app: str
    session: 'NawahSession'
    prev_session: MutableMapping
    prev_session_timeout: 'datetime'
    last_call: 'datetime'
    ws: 'WebSocketResponse'
    quota: 'NawahEnvQuota'
    args: MutableMapping[str, Any]


class NawahEnvQuota(TypedDict):
    '''Provides type-hint for 'quota' of 'Env' dict'''

    counter: int
    last_check: 'datetime'


class NawahSession(TypedDict):
    '''Provieds type-hint for 'session' of 'Env' dict'''

    _id: str
    user: MutableMapping
    groups: MutableSequence[str]
    host_add: str
    user_agent: str
    expiry: str
    token_hash: str
    create_time: str


class NawahQuerySpecialGroup(TypedDict):
    '''Provides type-hint for '$group' in 'NawahQuery' '''

    by: str
    count: int


class NawahQuerySpecialGeoNear(TypedDict):
    '''Provides type-hint for '$geo_near' in 'NawahQuery' '''

    val: str
    attr: str
    dist: int


# Following TypedDict type can't be defined as class as keys include $
NawahQuerySpecial = TypedDict(
    'NawahQuerySpecial',
    {
        '$search': str,
        '$sort': MutableMapping[str, Literal[1, -1]],
        '$skip': int,
        '$limit': int,
        '$extn': Union[bool, MutableSequence[str]],
        '$attrs': MutableSequence[str],
        '$group': MutableSequence[NawahQuerySpecialGroup],
        '$geo_near': NawahQuerySpecialGeoNear,
    },
    total=False,
)

NawahQueryOperEq = TypedDict('NawahQueryOperEq', {'$eq': Any})
NawahQueryOperNe = TypedDict('NawahQueryOperNe', {'$ne': Any})
NawahQueryOperGt = TypedDict('NawahQueryOperGt', {'$gt': Union[int, float, str]})
NawahQueryOperGte = TypedDict('NawahQueryOperGte', {'$gte': Union[int, float, str]})
NawahQueryOperLt = TypedDict('NawahQueryOperLt', {'$lt': Union[int, float, str]})
NawahQueryOperLte = TypedDict('NawahQueryOperLte', {'$lte': Union[int, float, str]})
NawahQueryOperAll = TypedDict('NawahQueryOperAll', {'$all': list[Any]})
NawahQueryOperIn = TypedDict('NawahQueryOperIn', {'$in': list[Any]})
NawahQueryOperNin = TypedDict('NawahQueryOperNin', {'$nin': list[Any]})
NawahQueryOperRegex = TypedDict('NawahQueryOperRegex', {'$regex': str})
NawahQueryStep = dict[
    str,
    Union[
        NawahQueryOperEq,
        NawahQueryOperNe,
        NawahQueryOperGt,
        NawahQueryOperGte,
        NawahQueryOperLt,
        NawahQueryOperLte,
        NawahQueryOperAll,
        NawahQueryOperIn,
        NawahQueryOperNin,
        NawahQueryOperRegex,
    ],
]

NawahQueryOperOr = TypedDict('NawahQueryOperOr', {'$or': list[NawahQueryStep]})

NawahQueryIndex = TypedDict(
    'NawahQueryIndex', {'$index': dict[str, list[tuple[str, Any]]]}
)

NawahQuery = TypedDict(
    'NawahQuery',
    {
        '$index': dict[str, list[tuple[str, Any]]],
        '$pipe': list[Union[NawahQueryStep, NawahQueryOperOr]],
        '$special': NawahQuerySpecial,
    },
    total=False,
)

NawahDoc = MutableMapping[str, Any]
