'''Provides 'Config', 'ConfigAttrSys' static classes'''

from typing import (TYPE_CHECKING, Any, Callable, MutableMapping,
                    MutableSequence, Optional, Set, Type, TypedDict)

from nawah.enums import LocaleStrategy

if TYPE_CHECKING:
    from datetime import datetime

    import redis.commands.json.JSON
    from bson import ObjectId
    from motor.motor_asyncio import AsyncIOMotorClient

    from nawah.classes import (L10N, Attr, ClientApp, Job, Module, SysDoc,
                               UserAttr)
    from nawah.types import (AnalyticsEvents, AppPackage, IPQuota, NawahDoc,
                             NawahEnv)


class VarTypeDict(TypedDict):
    '''Provides type-hint for item of 'vars_types' runtime config'''

    package: str
    type: 'Attr'


class ConfigAttrSys:
    '''ConfigAttrSys serves role of static class used as value for 'sys' attribute
    of 'Config' static class'''

    # pylint: disable=too-few-public-methods

    admin_check: bool = False

    conn: 'AsyncIOMotorClient'
    cache: Optional['redis.commands.json.JSON'] = None
    env: 'NawahEnv'
    docs: MutableMapping['ObjectId', 'SysDoc'] = {}
    jobs_base: 'datetime'

    nawah_version: str

    name: str
    version: str
    path: str
    packages: MutableMapping[str, 'AppPackage'] = {}

    cache_channels: Set[str] = set()

    sessions: MutableMapping[str, 'NawahEnv'] = {}
    session_counter = 0
    session_lock: Optional[float] = None
    ip_quota: MutableMapping[str, 'IPQuota'] = {}

    type_attrs: MutableSequence['Attr'] = []


class Config:
    '''Config serves role of static class used as central reference for runtime
    config of Nawah App'''

    # pylint: disable=too-few-public-methods

    debug: bool = False
    env: str
    port: int = 8081

    sys: Type[ConfigAttrSys] = ConfigAttrSys

    test: bool = False

    emulate_test: bool = False

    vars_types: MutableMapping[str, 'VarTypeDict'] = {}
    vars: MutableMapping[str, Any] = {}

    client_apps: MutableMapping[str, 'ClientApp'] = {}

    analytics_events: 'AnalyticsEvents' = {
        'app_conn_verified': True,
        'session_conn_auth': True,
        'session_user_auth': True,
        'session_conn_reauth': True,
        'session_user_reauth': True,
        'session_conn_deauth': True,
        'session_user_deauth': True,
    }

    conn_timeout: int = 120
    quota_anon_min: int = 40
    quota_auth_min: int = 100
    quota_ip_min: int = 500
    file_upload_limit: int = -1
    file_upload_timeout: int = 300

    data_server: str = 'mongodb://localhost'
    data_name: str = 'nawah_data'
    data_ssl: bool = False
    data_disk_use: bool = False

    cache_server: Optional[str] = None
    cache_db: Optional[int] = 0
    cache_username: Optional[str] = None
    cache_password: Optional[str] = None
    cache_expiry: Optional[int] = None

    error_reporting_server: Optional[str] = None

    locales: MutableSequence[str] = ['ar_AE', 'en_GB']
    locale: str = 'ar_AE'
    locale_strategy: 'LocaleStrategy' = LocaleStrategy.DUPLICATE

    admin_doc: 'NawahDoc' = {}
    admin_password: str

    anon_token: str
    anon_privileges: MutableMapping[str, MutableSequence[str]] = {}
    anon_doc: Optional['NawahDoc'] = None

    auth_attrs: MutableSequence[str] = []
    user_attrs_sanitise: MutableSequence[str] = []
    user_attrs: MutableMapping[str, 'UserAttr'] = {}

    groups: MutableSequence[MutableMapping[str, Any]] = []
    default_privileges: MutableMapping[str, MutableSequence[str]] = {}

    data_indexes: MutableSequence[MutableMapping[str, Any]] = []

    docs: MutableSequence['SysDoc'] = []

    l10n: MutableMapping[str, 'L10N'] = {}

    jobs: MutableMapping[str, 'Job'] = {}

    types: MutableMapping[str, Callable] = {}

    modules: MutableMapping[str, 'Module'] = {}
