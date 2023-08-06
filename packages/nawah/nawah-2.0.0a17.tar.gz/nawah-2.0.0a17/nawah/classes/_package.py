'''Provides 'Env', 'Package', 'App' dataclasses'''

from dataclasses import dataclass
from typing import (TYPE_CHECKING, Any, Callable, MutableMapping,
                    MutableSequence, Optional, Union)

if TYPE_CHECKING:
    from nawah.types import AnalyticsEvents, NawahDoc

    from ._attr import Attr
    from ._client_app import ClientApp
    from ._job import Job
    from ._l10n import L10N
    from ._module import Module
    from ._sys_doc import SysDoc
    from ._user_attr import UserAttr
    from ._var import Var


@dataclass(kw_only=True)
class Env:
    '''Env dataclass serves role of defining runtime environment config.
    It is used as item for 'envs' App Config Attr. It also serves as base
    for 'Package' dataclass'''

    # pylint: disable=too-many-instance-attributes

    debug: Union[bool, 'Var'] = False
    port: Optional[Union[int, 'Var']] = None
    emulate_test: bool = False
    desc: Optional[str] = None
    vars: Optional[MutableMapping[str, Any]] = None
    client_apps: Optional[MutableMapping[str, 'ClientApp']] = None
    analytics_events: Optional['AnalyticsEvents'] = None
    conn_timeout: Optional[Union[int, 'Var']] = None
    quota_anon_min: Optional[Union[int, 'Var']] = None
    quota_auth_min: Optional[Union[int, 'Var']] = None
    quota_ip_min: Optional[Union[int, 'Var']] = None
    file_upload_limit: Optional[Union[int, 'Var']] = None
    file_upload_timeout: Optional[Union[int, 'Var']] = None
    data_server: Optional[Union[str, 'Var']] = None
    data_name: Optional[Union[str, 'Var']] = None
    data_ssl: Optional[Union[bool, 'Var']] = None
    data_disk_use: Optional[Union[bool, 'Var']] = None
    cache_server: Optional[Union[str, 'Var']] = None
    cache_db: Optional[Union[int, 'Var']] = 0
    cache_username: Optional[Union[str, 'Var']] = None
    cache_password: Optional[Union[str, 'Var']] = None
    cache_expiry: Optional[Union[int, 'Var']] = None
    error_reporting_server: Optional[Union[str, 'Var']] = None
    locales: Optional[MutableSequence[str]] = None
    locale: Optional[str] = None
    l10n: Optional[MutableMapping[str, 'L10N']] = None
    admin_doc: Optional['NawahDoc'] = None
    admin_password: Optional['Var'] = None
    anon_token: Optional[str] = None
    anon_privileges: Optional[MutableMapping[str, MutableSequence[str]]] = None
    anon_doc: Optional['NawahDoc'] = None
    user_attrs: Optional[MutableMapping[str, 'UserAttr']] = None
    groups: Optional[MutableSequence[MutableMapping[str, Any]]] = None
    default_privileges: Optional[MutableMapping[str, MutableSequence[str]]] = None
    data_indexes: Optional[MutableSequence[MutableMapping[str, Any]]] = None
    docs: Optional[MutableSequence['SysDoc']] = None
    jobs: Optional[MutableMapping[str, 'Job']] = None
    types: Optional[MutableMapping[str, Callable]] = None


@dataclass(kw_only=True)
class Package(Env):
    '''Package dataclass serves role of defining Nawah Package and its config.
    It also serves as base for 'App' dataclass'''

    # pylint: disable=too-many-instance-attributes

    name: Optional[str] = None
    api_level: Optional[str] = None
    version: Optional[str] = None
    vars_types: Optional[MutableMapping[str, 'Attr']] = None
    modules: Optional[MutableSequence['Module']] = None

    def __post_init__(self):
        if self.name is None:
            raise Exception('Config Attr \'name\' should have value')


@dataclass(kw_only=True)
class App(Package):
    '''App dataclass serves role as defining Nawah App and its config'''

    # pylint: disable=too-many-instance-attributes

    name: Optional[str] = None
    version: Optional[str] = None
    env: Optional[Union[str, 'Var']] = None
    envs: Optional[MutableMapping[str, Env]] = None
    force_admin_check: Optional[bool] = None
    packages: Optional[MutableSequence['Package']] = None

    def __post_init__(self):
        if self.version is None:
            raise Exception('Config Attr \'version\' should have value')
