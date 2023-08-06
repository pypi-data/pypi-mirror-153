'''Provides 'serve_app' Utility'''

import asyncio
import logging
import re
from dataclasses import fields
from typing import TYPE_CHECKING, Any, MutableMapping, MutableSequence, cast

from nawah.classes import App, Attr, Default, Extn, Func, Perm, UserAttr, Var
from nawah.config import Config
from nawah.exceptions import ConfigException, InvalidVarException

from ._app import _run_app
from ._config import config_app, config_module
from ._val import deep_update, var_value
from ._validate import validate_attr, validate_type

if TYPE_CHECKING:
    from nawah.classes import Env, Package


logger = logging.getLogger('nawah')


def process_env_vars(config: 'Env', /):
    '''Checks all Var-prune Config Attrs of 'config' and updates value'''

    var_args: MutableMapping[str, MutableMapping[str, Any]] = {
        'debug': {'var': config.debug, 'type': bool, 'default': False},
        'port': {'var': config.port, 'type': int, 'default': 8081},
        'conn_timeout': {'var': config.conn_timeout, 'type': int},
        'quota_anon_min': {'var': config.quota_anon_min, 'type': int},
        'quota_auth_min': {'var': config.quota_auth_min, 'type': int},
        'quota_ip_min': {'var': config.quota_ip_min, 'type': int},
        'file_upload_limit': {
            'var': config.file_upload_limit,
            'type': int,
        },
        'file_upload_timeout': {
            'var': config.file_upload_timeout,
            'type': int,
        },
        'data_server': {'var': config.data_server, 'type': str},
        'data_name': {'var': config.data_name, 'type': str},
        'data_ssl': {'var': config.data_ssl, 'type': bool},
        'data_disk_use': {'var': config.data_disk_use, 'type': bool},
        'cache_server': {'var': config.cache_server, 'type': str},
        'cache_db': {
            'var': config.cache_db,
            'type': int,
            'default': 0,
        },
        'cache_username': {'var': config.cache_username, 'type': str},
        'cache_password': {'var': config.cache_password, 'type': str},
        'cache_expiry': {'var': config.cache_expiry, 'type': int},
        'error_reporting_server': {
            'var': config.error_reporting_server,
            'type': str,
        },
    }

    for arg_name, var_arg in var_args.items():
        if not isinstance(var_arg['var'], Var):
            continue
        try:
            setattr(
                config, arg_name, var_value(var_arg['var'], return_type=var_arg['type'])
            )
        except InvalidVarException as e:
            if 'default' not in var_arg:
                raise e
            setattr(config, arg_name, var_arg['default'])


def serve_app(app_config: 'App', /):
    '''Takes 'App' Object and setup runtime for it to run'''

    # pylint: disable=import-outside-toplevel

    from nawah.packages.core import core

    app_config_version = cast(str, app_config.version)

    if not re.match(r'^[0-9]+\.[0-9]+\.[0-9]+([ab][0-9]+)?$', app_config_version):
        raise ConfigException(
            f'App \'{app_config.name}\' defines invalid \'version\' \'{app_config.version}\''
        )

    # Check envs, env App Config Attr
    if app_config.envs and app_config.env:
        if isinstance(app_config.env, Var):
            logger.debug(
                'App \'{name}\' defines \'env\' App Config Attr as \'Var\' object. Getting its '
                'value..'
            )
            app_config.env = var_value(app_config.env)

        if app_config.env not in app_config.envs:
            raise ConfigException(
                'Value for \'env\' App Config Attr is \'{app_config.env}\', but'
                'no such Env is defined'
            )

        # Update runtime config with values from Env object
        app_config.env = cast(str, app_config.env)
        env = app_config.envs[app_config.env]
        for env_field in fields(env):
            if (env_attr_val := getattr(env, env_field.name)) is not None:
                # Specifically for l10n Config Attr, always update base value, and don't overwrite it
                if env_field.name == 'l10n':
                    # For a possibility app_config.l10n is None, set as L10N
                    if app_config.l10n is None:
                        app_config.l10n = {}
                    app_config.l10n.update(env_attr_val)
                else:
                    setattr(app_config, env_field.name, env_attr_val)

    if app_config.debug is True:
        logger.setLevel(logging.DEBUG)
        logger.debug('Set logging level to DEBUG (Config.debug==True)')

    if isinstance(app_config.debug, Var):
        try:
            if var_value(app_config.debug, return_type=lambda _: bool(int(_))):
                logger.setLevel(logging.DEBUG)
                logger.debug('Set logging level to DEBUG (Config.debug.var)')
                app_config.debug = True
        except InvalidVarException:
            logger.warning(
                'No value for \'Var\' object for \'debug\' App Config Attr. Logging '
                'remains at level ERROR'
            )

    logger.debug(
        'Getting value of \'Var\' object of \'admin_password\' App Config Attr..'
    )
    if isinstance(app_config.admin_password, Var):
        try:
            admin_password_val = var_value(app_config.admin_password)
            if not re.match(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.{8,})', admin_password_val
            ):
                raise Exception(
                    f'Value \'{admin_password_val}\' of \'admin_password\' App Config Attr doesn\'t '
                    'match accepted password format'
                )
            app_config.admin_password = admin_password_val
            Config.sys.admin_check = True
        except InvalidVarException:
            logger.warning(
                'No value for \'Var\' object for \'admin_password\' App Config Attr. \'ADMIN\' doc '
                'will not be checked or updated'
            )
            Config.sys.admin_check = False

    if isinstance(app_config.anon_token, Var):
        logger.debug(
            'App \'{name}\' defines \'anon_token\' App Config Attr as \'Var\' object. Getting its '
            'value..'
        )
        app_config.anon_token = var_value(app_config.anon_token)

    process_env_vars(app_config)

    configs: MutableSequence['Package'] = [
        core,
        *(app_config.packages or []),
        app_config,
    ]

    for config in configs:
        for config_field in fields(config):
            attr_name = config_field.name
            attr_val = getattr(config, attr_name, None)

            if attr_val is None:
                continue

            if attr_name in ['envs', 'api_level', 'version', 'modules', 'packages']:
                continue

            # For user_attrs, process separatly to update user module
            if attr_name == 'user_attrs':
                user_module = Config.modules['user']
                for user_attr_name, user_attr in cast(
                    MutableMapping[str, 'UserAttr'], config.user_attrs
                ).items():
                    if not isinstance(user_attr, UserAttr):
                        raise ConfigException(
                            f'Invalid type for attr \'{user_attr_name}\' defined for package '
                            f'\'{config.name}\' for \'user_attrs\' Config Attr'
                        )
                    if user_attr_name in user_module.attrs:
                        raise ConfigException(
                            f'Package \'{config.name}\' defines \'user_attrs\' Config Attr with '
                            f'conflicting attr \'{user_attr_name}\''
                        )
                    if not isinstance(user_attr.type, Attr):
                        raise ConfigException(
                            f'Invalid type for attr type \'{user_attr_name}\' defined for package '
                            f'\'{config.name}\' for \'user_attrs\' Config Attr'
                        )

                    Config.user_attrs[user_attr_name] = user_attr
                    user_module.attrs[user_attr_name] = user_attr.type

                    if user_attr.sanitise:
                        Config.user_attrs_sanitise.append(user_attr_name)

                    if user_attr.auth_attr:
                        Config.auth_attrs.append(user_attr_name)
                        Config.user_attrs_sanitise.append(f'{user_attr_name}_hash')
                        user_module.unique_attrs.append(user_attr_name)
                        user_module.attrs[f'{user_attr_name}_hash'] = Attr.STR()
                        session_auth_doc_args = cast(
                            MutableSequence[MutableMapping[str, 'Attr']],
                            Config.modules['session'].funcs['auth'].doc_attrs,
                        )
                        session_auth_doc_args.extend(
                            [
                                {
                                    'hash': Attr.STR(),
                                    user_attr_name: user_attr.type,
                                    'groups': Attr.LIST(list=[Attr.ID()]),
                                },
                                {'hash': Attr.STR(), user_attr_name: user_attr.type},
                            ]
                        )

                    if user_attr.default:
                        if not isinstance(user_attr.default, Default):
                            raise ConfigException(
                                f'Invalid type for attr default \'{user_attr_name}\' defined for '
                                f'package \'{config.name}\' for \'user_attrs\' Config Attr'
                            )
                        user_module.defaults[user_attr_name] = user_attr.default

                    if user_attr.extn:
                        if not isinstance(user_attr.extn, Extn):
                            raise ConfigException(
                                f'Invalid type for attr extn \'{user_attr_name}\' defined for '
                                f'package \'{config.name}\' for \'user_attrs\' Config Attr'
                            )
                        user_module.extns[user_attr_name] = user_attr.extn

                    if user_attr.func:
                        # [TODO] Expanded type validation for Func
                        if not isinstance(user_attr.type, Func):
                            raise ConfigException(
                                f'Invalid type for attr func \'{user_attr_name}\' defined for '
                                f'package \'{config.name}\' for \'user_attrs\' Config Attr'
                            )
                        user_module.funcs[f'update_{user_attr_name}'] = user_attr.func
                    else:
                        user_module.funcs[f'update_{user_attr_name}'] = Func(
                            permissions=[Perm(privilege=user_attr_name)],
                            query_attrs={'_id': Attr.ID()},
                            doc_attrs={user_attr_name: user_attr.type},
                            strict_doc=True,
                        )

                    user_module.funcs[
                        f'update_{user_attr_name}'
                    ].name = f'update_{user_attr_name}'
                    user_module.funcs[f'update_{user_attr_name}'].module = user_module

            # For vars_types Config Attr, preserve config name for debugging purposes
            elif attr_name == 'vars_types':
                for var in attr_val:
                    config.name = cast(str, config.name)
                    Config.vars_types[var] = {
                        'package': config.name,
                        'type': attr_val[var],
                    }

            # Otherwise, update Config accroding to attr_val type
            elif isinstance(attr_val, list):
                for j in attr_val:
                    getattr(Config, attr_name).append(j)
                if attr_name == 'locales':
                    Config.locales = list(set(Config.locales))

            elif isinstance(attr_val, dict):
                if not getattr(Config, attr_name):
                    setattr(Config, attr_name, {})
                deep_update(target=getattr(Config, attr_name), new_values=attr_val)

            else:
                setattr(Config, attr_name, attr_val)

        if config.modules:
            config_modules = []
            for module in config.modules:
                if module.name in Config.modules:
                    raise ConfigException(
                        f'Module \'{module.name}\' exist in current runtime config'
                    )

                config_module(module_name=module.name, module=module)
                config_modules.append(module.name)
                Config.modules[module.name] = module

            Config.sys.packages[config.name or ''] = {
                'package': config,
                'modules': config_modules,
            }

        if getattr(config, 'packages', None):
            pass

        if isinstance(config, App):
            Config.sys.name = config.name or ''
            Config.sys.version = config.version or ''

    # Update User, Session modules with populated attrs
    Config.modules['user'].defaults['locale'] = Default(value=Config.locale)

    # [DOC] Attempt to validate all packages required vars (via vars_types Config Attr) are met
    for var_name, var in Config.vars_types.items():
        if var_name not in Config.vars:
            raise ConfigException(
                f'Package \'{var["package"]}\' requires \'{var_name}\' Var, but not found in App '
                'Config'
            )
        try:
            validate_attr(
                mode='create',
                attr_name=var_name,
                attr_type=var['type'],
                attr_val=Config.vars[var_name],
            )
        except Exception as e:
            raise ConfigException(
                f'Package \'{var["package"]}\' requires \'{var_name}\' Var of type '
                f'\'{var["type"].type}\', but validation failed'
            ) from e

    # Validate Attr Type of type TYPE. Has to run before config_app so calls in config_app
    # depending on such attrs don't fail
    for attr_type in Config.sys.type_attrs:
        validate_type(attr_type=attr_type)

    asyncio.run(config_app())

    # Attempt to call post_config callable of all modules
    for module_name, module in Config.modules.items():
        logger.debug(
            'Attempting to check for \'post_config\' callable for module: %s',
            module_name,
        )
        if not module.post_config:
            logger.debug('- Module does not define \'post_config\' callable')
            continue

        logger.debug('- Module does define \'post_config\' callable. Calling it..')
        asyncio.run(module.post_config())

    _run_app()
