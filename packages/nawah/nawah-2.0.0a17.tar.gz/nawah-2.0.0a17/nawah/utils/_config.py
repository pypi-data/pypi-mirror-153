'''Provides utilities required for configuring modules, packages and app'''

import copy
import datetime
import logging
import os
from typing import TYPE_CHECKING, Any, MutableMapping, cast

import sentry_sdk
from bson import ObjectId
from croniter import croniter
from passlib.hash import pbkdf2_sha512
from redis import asyncio as aioredis  # type: ignore

from nawah.classes import Attr, Counter, Default, Diff, Extn, Func, SysDoc
from nawah.config import Config
from nawah.enums import AttrType, Event
from nawah.exceptions import (ConfigException, InvalidAttrTypeArgException,
                              InvalidAttrTypeException)

from ._attr_type import extract_attr, generate_attr_val
from ._call import call
from ._validate._type import validate_type

if TYPE_CHECKING:
    from nawah.classes import Module
    from nawah.types import NawahDoc

logger = logging.getLogger('nawah')


def config_module(*, module_name: str, module: 'Module'):
    '''Validates args for 'module' and updates values for 'attrs' of 'module' per sets from
    'defaults', 'extns', 'counters' '''

    # pylint: disable=import-outside-toplevel

    import nawah.base as Base

    # Set name of module in Module object for reverse reference
    module.name = module_name

    logger.debug('Attempting to configure module \'%s\'', module_name)

    if not module.funcs:
        raise ConfigException(f'Module \'{module_name}\' doesn\'t define any function')

    for func_name, func in module.funcs.items():
        logger.debug(
            'Attempting to validate Function \'%s\'.\'%s\'', module_name, func_name
        )
        func.name = func_name
        func.module = module
        # Check value type
        if not isinstance(func, Func):
            raise ConfigException(
                f'Invalid Nawah Function for \'{module_name}\'.\'{func_name}\' of type '
                '\'{type(func)}\''
            )

        # Validate query_attrs, doc_attrs, call_args
        for func_attr_name in ['query_attrs', 'doc_attrs', 'call_args']:
            logger.debug(
                'Attempting to validate \'%s\' of \'%s\'.\'%s\'',
                func_attr_name,
                module_name,
                func_name,
            )
            if func_attr_val := getattr(func, func_attr_name):
                # query_attrs, doc_attrs are lists of dicts, call_args is just dict
                # Do this trick to get this loop to work nonetheless, by wrapping call_args with
                # a list, to let the rest of the loop deal with theree attrs in same manner
                if func_attr_name == 'call_args':
                    func_attr_val = [func_attr_val]
                for attrs_set in func_attr_val:
                    for attr_name, attr_type in attrs_set.items():
                        try:
                            logger.debug(
                                'Attempting to validate \'%s\' Attr Type of \'%s\' for Function '
                                '\'%s\'.\'%s\' of set \'%s\'',
                                func_attr_name,
                                attr_name,
                                module_name,
                                func.name,
                                attrs_set,
                            )
                            validate_type(attr_type=attr_type, skip_type=True)
                        except InvalidAttrTypeException as e:
                            raise ConfigException(
                                f'Invalid Attr Type for \'{module_name}\'.\'{attr_name}\'. '
                                f'Original validation error: {str(e)}',
                            ) from e
                        except InvalidAttrTypeArgException as e:
                            raise ConfigException(
                                f'Invalid Attr Type Arg for \'{module_name}\'.\'{attr_name}\'. '
                                f'Original validation error: {str(e)}'
                            ) from e

        # [TODO] Add steps to update Func object attributes per func callable
        # If Func has callable defined skip
        if func.callable:
            if not callable(func.callable):
                raise ConfigException(
                    f'Value \'callable\' for Nawah Function \'{func_name}\' of \'{module_name}\' '
                    'is not callable'
                )
            continue

        logger.debug(
            'Function \'%s\'.\'%s\' doesn\'t define callable. Attempting to set per name',
            module_name,
            func_name,
        )
        # Otherwise, set callable based on fucntion name, update query_attrs, doc_attrs, call_args
        if func_name.startswith('create_file'):
            func.doc_attrs = [
                {
                    'attr': Attr.STR(),
                    'lastModified': Attr.INT(),
                    'type': Attr.STR(),
                    'name': Attr.STR(),
                    'content': Attr(
                        desc='',
                        type=AttrType.BYTES,
                        args={},
                    ),
                },
                {'_id': Attr.ID(), 'doc': Attr.ID()},
            ]
            func.post_func = True
            func.callable = Base.create_file

        elif func_name.startswith('update_file'):
            func.post_func = True
            func.callable = Base.update_file

        elif func_name.startswith('delete_file'):
            func.post_func = True
            func.callable = Base.delete_file

        elif func_name.startswith('delete_lock'):
            func.callable = Base.delete_lock

        elif func_name.startswith('obtain_lock'):
            func.callable = Base.obtain_lock

        elif func_name.startswith('read_diff'):
            func.callable = Base.read_diff

        elif func_name.startswith('retrieve_file'):
            func.query_attrs = [
                {
                    '_id': Attr.ID(),
                    'attr': Attr.STR(),
                    'filename': Attr.STR(),
                },
                {
                    '_id': Attr.ID(),
                    'attr': Attr.STR(),
                    'thumb': Attr.STR(pattern=r'[0-9]+x[0-9]+'),
                    'filename': Attr.STR(),
                },
            ]
            func.get_func = True
            func.callable = Base.retrieve_file

        elif func_name.startswith('read'):
            func.callable = Base.read

        elif func_name.startswith('create'):
            func.callable = Base.create

        elif func_name.startswith('update'):
            func.callable = Base.update

        elif func_name.startswith('delete'):
            func.callable = Base.delete

        else:
            raise ConfigException(
                f'Can\'t set callable for Nawah Function \'{func_name}\' of'
                f' \'{module_name}\''
            )

        if not func.call_args:
            func.call_args = {}

        func.call_args.update({'raise_no_success': Attr.BOOL()})

    # Check attrs for any invalid type
    for attr in module.attrs:
        try:
            logger.debug(
                'Attempting to validate Attr Type for \'%s\'.\'%s\'',
                module_name,
                attr,
            )
            validate_type(attr_type=module.attrs[attr], skip_type=True)
        except InvalidAttrTypeException as e:
            raise ConfigException(
                f'Invalid Attr Type for \'{module_name}\'.\'{attr}\'. Original '
                f'validation error: {str(e)}',
            ) from e
        except InvalidAttrTypeArgException as e:
            raise ConfigException(
                f'Invalid Attr Type Arg for \'{module_name}\'.\'{attr}\'. Original '
                f'validation error: {str(e)}'
            ) from e

    # Check defaults for invalid types, update default value
    for attr_name, default in module.defaults.items():
        if not isinstance(default, Default):
            raise ConfigException(
                f'Invalid Default Instruction for \'{module_name}\'.\'{attr_name}\', of type '
                f'\'{type(default)}\''
            )

        logger.debug(
            'Updating default value for attr \'%s\' to: \'%s\'',
            attr_name,
            module.defaults[attr_name],
        )
        extract_attr(attrs=module.attrs, path=attr_name).default = module.defaults[
            attr_name
        ]

    # Check counters for invalid attrs, types
    for attr_name, counter in module.counters.items():
        if not isinstance(counter, Counter):
            raise ConfigException(
                f'Invalid Counter Instruction for \'{module_name}\'.\'{attr_name}\', of type '
                f'\'{type(counter)}\''
            )

        if attr_name not in module.attrs:
            raise ConfigException(
                f'Invalid attr for Counter Instruction. Module \'{module_name}\' '
                f'doesn\'t have top-level attr \'{attr_name}\''
            )

        if module.attrs[attr_name].type != AttrType.ANY:
            raise ConfigException(
                f'Attr \'{module_name}\'.\'{attr_name}\' for Counter Instruction can only be of '
                'Attr Type ANY'
            )

        # Set default value to Default(value=None) to skip InvalidAttrException when checking doc
        module.attrs[attr_name].default = Default(value=None)

    # Update extn value
    for attr_name, extn in module.extns.items():
        if not isinstance(extn, Extn):
            raise ConfigException(
                f'Invalid Extension Instruction for \'{module_name}\'.\'{attr_name}\', of type '
                f'\'{type(extn)}\''
            )

        logger.debug(
            'Updating \'extn\' for attr \'%s\' to: \'%s\'',
            attr_name,
            module.extns[attr_name],
        )
        extract_attr(attrs=module.attrs, path=attr_name).extn = module.extns[attr_name]

    # Check extns for invalid extended attrs
    for attr_name, extn in module.extns.items():
        if not isinstance(extn, Extn):
            raise ConfigException(
                f'Invalid extns attr \'{attr_name}\' of module \'{module_name}\''
            )

    # Check valid type, value for diff
    if module.diff is not None and not isinstance(module.diff, Diff):
        raise ConfigException(f'Invalid Diff Instruction for module \'{module_name}\'')

    if isinstance(module.diff, Attr):
        module.diff = cast(Attr, module.diff)
        if module.diff.type != AttrType.TYPE:
            raise ConfigException(
                f'Invalid Attr Type for diff of module \'{module_name}\'. Only Attr Type TYPE '
                'is allowed'
            )
        logger.debug(
            'Attempting to validate Attr Type diff of module \'%s\'', module_name
        )
        try:
            validate_type(attr_type=module.diff)
        except InvalidAttrTypeException as e:
            raise ConfigException(
                f'Invalid Attr Type for diff of module \'{module_name}\'. Original validation error: {str(e)}'
            ) from e
        except InvalidAttrTypeArgException as e:
            raise ConfigException(
                f'Invalid Attr Type Arg for diff of module \'{module_name}\'. Original validation error: {str(e)}'
            ) from e

    # [TODO] Re-implement
    # Check valid types, values for create_draft, update_draft
    # for attr in ['create_draft', 'update_draft']:
    #     if type(getattr(self, attr)) not in [bool, Attr]:
    #         raise ConfigException(f'Invalid {attr} for module \'{module_name}\'') from e
    #     if type(getattr(self, attr)) == Attr:
    #         if getattr(self, attr).type != AttrType.TYPE:
    #             raise ConfigException(
    #                 f'Invalid Attr Type for {attr} of module \'{module_name}\'. Only Attr Type TYPE is allowed'
    #             ) from e
    #         logger.debug(
    #             f'Attempting to validate Attr Type {attr} of module \'{module_name}\'.'
    #         )
    #         try:
    #             validate_type(attr_type=getattr(self, attr))
    #         except InvalidAttrTypeException as e:
    #             raise ConfigException(
    #                 f'Invalid Attr Type for {attr} of module \'{module_name}\'. Original validation error: {str(e)}'
    #             ) from e
    #         except InvalidAttrTypeArgException as e:
    #             raise ConfigException(
    #                 f'Invalid Attr Type Arg for {attr} of module \'{module_name}\'. Original validation error: {str(e)}'
    #             ) from e

    logger.debug('Configured module %s', module_name)


async def config_app():

    # [TODO] Re-implement
    # Check API version
    # nawah_level = '.'.join(Config.sys.version.split('.')[0:2])
    # for package, api_level in {
    #     name: config['package'].api_level
    #     for name, config in Config.sys.packages.items()
    # }.items():
    #     if api_level != nawah_level:
    #         raise ConfigException(
    #             f'Nawah framework is on API-level \'{nawah_level}\', but the app package'
    #             f'\'{package}\' requires API-level \'{api_level}\''
    #         )
    # try:
    #     versions = (
    #         (
    #             requests.get(
    #                 'https://raw.githubusercontent.com/masaar/nawah_versions/master/versions.txt'
    #             ).content
    #         )
    #         .decode('utf-8')
    #         .split('\n')
    #     )
    #     version_detected = ''
    #     for version in versions:
    #         if version.startswith(f'{nawah_level}.'):
    #             if version_detected and int(version.split('.')[-1]) < int(
    #                 version_detected.split('.')[-1]
    #             ):
    #                 continue
    #             version_detected = version
    #     if version_detected and version_detected != Config.sys.version:
    #         logger.warning(
    #             f'Your app is using Nawah version \'{Config.sys.version}\' while newer version \'{version_detected}\' of the API-level is available. Please, update'
    #         )
    # except:
    #     logger.warning(
    #         'An error occurred while attempting to check for latest update to Nawah. Please, check for updates on your own'
    #     )

    # Check for jobs
    if Config.jobs:
        # Check jobs schedule validity
        Config.sys.jobs_base = datetime.datetime.utcnow()
        for job_name, job in Config.jobs.items():
            if not croniter.is_valid(job.schedule):
                raise ConfigException(
                    f'Job with schedule \'{job_name}\' schedule is invalid'
                )

            job.cron_schedule = croniter(job.schedule, Config.sys.jobs_base)
            job.next_time = datetime.datetime.fromtimestamp(
                job.cron_schedule.get_next(), datetime.timezone.utc
            ).isoformat()[:16]

    # Check for presence of user_attrs
    if not Config.user_attrs:
        raise ConfigException('No \'user_attrs\' are provided')

    # Check for Env Vars
    attrs_defaults = {
        'data_server': 'mongodb://localhost',
        'data_name': 'nawah_data',
        'data_ssl': False,
        'emulate_test': False,
    }
    for attr_name in attrs_defaults:
        attr_val = getattr(Config, attr_name)
        if type(attr_val) == str and attr_val.startswith('$__env.'):
            logger.debug(f'Detected Env Variable for config attr \'{attr_name}\'')
            if not os.getenv(attr_val[7:]):
                logger.warning(
                    f'Couldn\'t read Env Variable for config attr \'{attr_name}\'. Defaulting to \'{attrs_defaults[attr_name]}\''
                )
                setattr(Config, attr_name, attrs_defaults[attr_name])
            else:
                # Set data_ssl to True rather than string Env Variable value
                if attr_name == 'ssl':
                    attr_val = True
                else:
                    attr_val = os.getenv(attr_val[7:])
                logger.warning(
                    f'Setting Env Variable for config attr \'{attr_name}\' to \'{attr_val}\''
                )
                setattr(Config, attr_name, attr_val)

    from nawah import data as Data

    # Create default env dict
    anon_user = _compile_anon_user()
    anon_session = _compile_anon_session()
    anon_session['user'] = anon_user
    Config.sys.conn = Data.create_conn()
    Config.sys.env = {
        'conn': Config.sys.conn,
        'REMOTE_ADDR': '127.0.0.1',
        'HTTP_USER_AGENT': 'Nawah',
        'client_app': '__sys',
        'session': anon_session,
    }

    # Check cache_server Config Attr
    if Config.cache_server:
        logger.debug('Attempting to create connection with \'cache_server\'')
        Config.sys.cache = aioredis.Redis(
            host=Config.cache_server,
            db=Config.cache_db,
            username=Config.cache_username,
            password=Config.cache_password,
        ).json()

    # Check error_reporting_server Config Attr
    if Config.error_reporting_server:
        logger.debug('Attempting to create connection with \'error_reporting_server\'')
        sentry_sdk.init(  # pylint: disable=abstract-class-instantiated
            Config.error_reporting_server,
            traces_sample_rate=1.0,
            with_locals=True,
            release=f'{Config.sys.name}:{Config.sys.version}',
            environment=Config.env,
        )

    # Check test mode
    if Config.test:
        logger.debug('Test mode detected')
        logger.setLevel(logging.DEBUG)
        __location__ = os.path.realpath(os.path.join('.'))
        if not os.path.exists(os.path.join(__location__, 'tests')):
            os.makedirs(os.path.join(__location__, 'tests'))
        for module_name, module in Config.modules.items():
            module_collection = module.collection
            logger.debug(
                f'Updating collection name \'{module_collection}\' of module {module_name}'
            )
            module_collection = module.collection = f'test_{module_collection}'

            logger.debug(f'Flushing test collection \'{module_collection}\'')
            await Data.drop(
                env=Config.sys.env,
                collection_name=module_collection,
            )

    # Checking users collection
    # [TODO] Updated sequence to handle users
    logger.debug('Testing users collection')
    if Config.sys.admin_check:
        user_results = await call(
            'user/read',
            # [TODO] Check behaviour with removed Event.ON
            skip_events=[Event.PERM],
            env=Config.sys.env,
            query=[{'_id': 'f00000000000000000000010'}],
        )
        if not user_results['args']['count']:
            logger.debug('ADMIN user not found, creating it')
            # Prepare base ADMIN user doc
            admin_create_doc = {
                '_id': ObjectId('f00000000000000000000010'),
                'name': {Config.locale: '__ADMIN'},
                'groups': [],
                'privileges': {'*': ['*']},
                'locale': Config.locale,
            }
            # Update ADMIN user doc with admin_doc Config Attr
            admin_create_doc.update(Config.admin_doc)

            for auth_attr in Config.user_attrs:
                admin_create_doc[f'{auth_attr}_hash'] = pbkdf2_sha512.using(
                    rounds=100000
                ).hash(
                    f'{auth_attr}{admin_create_doc[auth_attr]}{Config.admin_password}'
                    f'{Config.anon_token}'.encode('utf-8')
                )
            admin_results = await call(
                'user/create',
                skip_events=[Event.PERM],
                env=Config.sys.env,
                doc=admin_create_doc,
            )
            logger.debug('ADMIN user creation results: %s', admin_results)
            if admin_results['status'] != 200:
                raise ConfigException('Config step failed')
        else:
            logger.debug(
                '\'ADMIN\' doc found. Attempting to check if update is required..'
            )
            admin_doc = user_results['args']['docs'][0]
            admin_doc_update = {}
            for attr_name, attr_val in Config.admin_doc.items():
                if (
                    attr_name not in admin_doc
                    or not admin_doc[attr_name]
                    or attr_val != admin_doc[attr_name]
                ):
                    if (
                        isinstance(attr_val, dict)
                        and Config.locale in attr_val
                        and isinstance(admin_doc[attr_name], dict)
                        and (
                            (
                                Config.locale in admin_doc[attr_name]
                                and attr_val[Config.locale]
                                == admin_doc[attr_name][Config.locale]
                            )
                            or (Config.locale not in admin_doc[attr_name])
                        )
                    ):
                        continue
                    logger.debug(
                        'Detected change in \'admin_doc.%s\' Config Attr', attr_name
                    )
                    admin_doc_update[attr_name] = attr_val
            for auth_attr in Config.user_attrs:
                auth_attr_hash = pbkdf2_sha512.using(rounds=100000).hash(
                    f'{auth_attr}{admin_doc[auth_attr]}{Config.admin_password}'
                    f'{Config.anon_token}'.encode('utf-8')
                )
                if (
                    f'{auth_attr}_hash' not in admin_doc
                    or auth_attr_hash != admin_doc[f'{auth_attr}_hash']
                ):
                    logger.debug(f'Detected change in \'admin_password\' Config Attr')
                    admin_doc_update[f'{auth_attr}_hash'] = auth_attr_hash
            if len(admin_doc_update.keys()):
                logger.debug(
                    f'Attempting to update ADMIN user with doc: \'{admin_doc_update}\''
                )
                admin_results = await call(
                    'user/update',
                    # [TODO] Check behaviour with removed Event.ON
                    # [TODO] Check behaviour with removed Event.PRE
                    skip_events=[Event.PERM],
                    env=Config.sys.env,
                    query=[{'_id': ObjectId('f00000000000000000000010')}],
                    doc=admin_doc_update,
                )
                logger.debug(f'ADMIN user update results: {admin_results}')
                if admin_results['status'] != 200:
                    raise ConfigException('Config step failed')
            else:
                logger.debug('ADMIN user is up-to-date')
    else:
        logger.warning(
            'Skipping checking \'ADMIN\' doc due to \'sys.admin_check\' Config Attr'
        )

    Config.sys.docs[ObjectId('f00000000000000000000010')] = SysDoc(module='user')

    # Test if ANON user exists
    user_results = await call(
        'user/read',
        # [TODO] Check behaviour with removed Event.ON
        skip_events=[Event.PERM],
        env=Config.sys.env,
        query=[{'_id': 'f00000000000000000000011'}],
    )
    if not user_results['args']['count']:
        logger.debug('ANON user not found, creating it')
        anon_results = await call(
            'user/create',
            # [TODO] Check behaviour with removed Event.ON
            # [TODO] Check behaviour with removed Event.PRE
            skip_events=[Event.PERM],
            env=Config.sys.env,
            doc=_compile_anon_user(),
        )
        logger.debug(f'ANON user creation results: {anon_results}')
        if anon_results['status'] != 200:
            raise ConfigException('Config step failed')
    else:
        logger.debug('ANON user found, checking it')
        anon_doc = _compile_anon_user()
        anon_doc_update = {}
        for attr in Config.user_attrs:
            if attr not in anon_doc or not anon_doc[attr]:
                logger.debug(f'Detected change in \'anon_doc.{attr}\' Config Attr')
                anon_doc_update[attr] = generate_attr_val(
                    attr_type=Config.user_attrs[attr].type
                )
        for module in Config.anon_privileges:
            if module not in anon_doc or set(anon_doc[module]) != set(
                Config.anon_privileges[module]
            ):
                logger.debug(f'Detected change in \'anon_privileges\' Config Attr')
                anon_doc_update[f'privileges.{module}'] = Config.anon_privileges[module]
        for auth_attr in Config.user_attrs:
            if (
                f'{auth_attr}_hash' not in anon_doc
                or anon_doc[f'{auth_attr}_hash'] != Config.anon_token
            ):
                logger.debug(f'Detected change in \'anon_token\' Config Attr')
                anon_doc_update[attr] = Config.anon_token
            anon_doc_update[f'{auth_attr}_hash'] = Config.anon_token
        if len(anon_doc_update.keys()):
            logger.debug(
                f'Attempting to update ANON user with doc: \'{anon_doc_update}\''
            )
            anon_results = await call(
                'user/update',
                # [TODO] Check behaviour with removed Event.ON
                # [TODO] Check behaviour with removed Event.PRE
                skip_events=[Event.PERM],
                env=Config.sys.env,
                query=[{'_id': ObjectId('f00000000000000000000011')}],
                doc=anon_doc_update,
            )
            logger.debug(f'ANON user update results: {anon_results}')
            if anon_results['status'] != 200:
                raise ConfigException('Config step failed')
        else:
            logger.debug('ANON user is up-to-date')

    Config.sys.docs[ObjectId('f00000000000000000000011')] = SysDoc(module='user')

    logger.debug('Testing sessions collection')
    # Test if ANON session exists
    session_results = await call(
        'session/read',
        # [TODO] Check behaviour with removed Event.ON
        skip_events=[Event.PERM],
        env=Config.sys.env,
        query=[{'_id': 'f00000000000000000000012'}],
    )
    if not session_results['args']['count']:
        logger.debug('ANON session not found, creating it')
        anon_results = await call(
            'session/create',
            # [TODO] Check behaviour with removed Event.ON
            # [TODO] Check behaviour with removed Event.PRE
            skip_events=[Event.PERM],
            env=Config.sys.env,
            doc=_compile_anon_session(),
        )
        logger.debug(f'ANON session creation results: {anon_results}')
        if anon_results['status'] != 200:
            raise ConfigException('Config step failed')
    Config.sys.docs[ObjectId('f00000000000000000000012')] = SysDoc(module='session')

    logger.debug('Testing groups collection')
    # Test if DEFAULT group exists
    group_results = await call(
        'group/read',
        # [TODO] Check behaviour with removed Event.ON
        skip_events=[Event.PERM],
        env=Config.sys.env,
        query=[{'_id': 'f00000000000000000000013'}],
    )
    if not group_results['args']['count']:
        logger.debug('DEFAULT group not found, creating it')
        group_create_doc = {
            '_id': ObjectId('f00000000000000000000013'),
            'user': ObjectId('f00000000000000000000010'),
            'name': {locale: '__DEFAULT' for locale in Config.locales},
            'bio': {locale: '__DEFAULT' for locale in Config.locales},
            'privileges': Config.default_privileges,
        }
        group_results = await call(
            'group/create',
            # [TODO] Check behaviour with removed Event.ON
            # [TODO] Check behaviour with removed Event.PRE
            skip_events=[Event.PERM],
            env=Config.sys.env,
            doc=group_create_doc,
        )
        logger.debug('DEFAULT group creation results: %s', group_results)
        if group_results['status'] != 200:
            raise ConfigException('Config step failed')
    else:
        logger.debug('DEFAULT group found, checking it')
        default_doc = group_results['args']['docs'][0]
        default_doc_update: MutableMapping[str, Any] = {}
        for module in Config.default_privileges:
            if module not in default_doc['privileges'].keys() or set(
                default_doc['privileges'][module]
            ) != set(Config.default_privileges[module]):
                logger.debug('Detected change in \'default_privileges\' Config Attr')
                default_doc_update[f'privileges.{module}'] = Config.default_privileges[
                    module
                ]
        if len(default_doc_update.keys()):
            logger.debug(
                'Attempting to update DEFAULT group with doc: \'%s\'',
                default_doc_update,
            )
            default_results = await call(
                'group/update',
                # [TODO] Check behaviour with removed Event.ON
                # [TODO] Check behaviour with removed Event.PRE
                skip_events=[Event.PERM],
                env=Config.sys.env,
                query=[{'_id': ObjectId('f00000000000000000000013')}],
                doc=default_doc_update,
            )
            logger.debug(f'DEFAULT group update results: {default_results}')
            if anon_results['status'] != 200:
                raise ConfigException('Config step failed')
        else:
            logger.debug('DEFAULT group is up-to-date')

    Config.sys.docs[ObjectId('f00000000000000000000013')] = SysDoc(module='group')

    # Test app-specific groups
    logger.debug('Testing app-specific groups collection')
    for group in Config.groups:
        group_results = await call(
            'group/read',
            # [TODO] Check behaviour with removed Event.ON
            skip_events=[Event.PERM],
            env=Config.sys.env,
            query=[{'_id': group['_id']}],
        )
        if not group_results['args']['count']:
            logger.debug(
                f'App-specific group with name \'{group["name"]}\' not found, creating it'
            )
            group_results = await call(
                'group/create',
                # [TODO] Check behaviour with removed Event.ON
                # [TODO] Check behaviour with removed Event.PRE
                skip_events=[Event.PERM],
                env=Config.sys.env,
                doc=group,
            )
            logger.debug(
                f'App-specific group with name {group["name"]} creation results: {group_results}'
            )
            if group_results['status'] != 200:
                raise ConfigException('Config step failed')
        else:
            logger.debug(
                f'App-specific group with name \'{group["name"]}\' found, checking it'
            )
            group_doc = group_results['args']['docs'][0]
            group_doc_update = {}
            if 'privileges' in group:
                for module in group['privileges']:
                    if module not in group_doc['privileges'].keys() or set(
                        group_doc['privileges'][module]
                    ) != set(group['privileges'][module]):
                        logger.debug(
                            f'Detected change in \'privileges\' Doc Arg for group with name \'{group["name"]}\''
                        )
                        group_doc_update[f'privileges.{module}'] = group['privileges'][
                            module
                        ]
            if len(group_doc_update.keys()):
                logger.debug(
                    'Attempting to update group with name \'%s\' with doc: \'%s\'',
                    group['name'],
                    group_doc_update,
                )
                group_results = await call(
                    'group/update',
                    # [TODO] Check behaviour with removed Event.ON
                    # [TODO] Check behaviour with removed Event.PRE
                    skip_events=[Event.PERM],
                    env=Config.sys.env,
                    query=[{'_id': group['_id']}],
                    doc=group_doc_update,
                )
                logger.debug(
                    'Group with name \'%s\' update results: %s',
                    group['name'],
                    group_results,
                )
                if group_results['status'] != 200:
                    raise ConfigException('Config step failed')
            else:
                logger.debug('Group with name \'%s\' is up-to-date', group['name'])

        Config.sys.docs[ObjectId(group['_id'])] = SysDoc(module='group')

    # Test app-specific data indexes
    logger.debug('Testing data indexes')
    for index in Config.data_indexes:
        logger.debug('Attempting to create data index: %s', index)
        try:
            Config.sys.conn[Config.data_name][index['collection']].create_index(
                index['index']
            )
        except Exception as e:
            logger.error('Failed to create data index: %s, with error: %s', index, e)
            logger.error('Evaluate error and take action manually')

    logger.debug(
        'Creating \'var\', \'type\', \'user\' data indexes for settings collections'
    )
    Config.sys.conn[Config.data_name]['settings'].create_index([('var', 1)])
    Config.sys.conn[Config.data_name]['settings'].create_index([('type', 1)])
    Config.sys.conn[Config.data_name]['settings'].create_index([('user', 1)])
    logger.debug(
        'Creating \'user\', \'event\', \'subevent\' data indexes for analytics collections'
    )
    Config.sys.conn[Config.data_name]['analytics'].create_index([('user', 1)])
    Config.sys.conn[Config.data_name]['analytics'].create_index([('event', 1)])
    Config.sys.conn[Config.data_name]['analytics'].create_index([('subevent', 1)])
    logger.debug('Creating \'__deleted\' data indexes for all collections')
    for module in Config.modules:
        if Config.modules[module].collection:
            logger.debug(
                'Attempting to create \'__deleted\' data index for collection: %s',
                Config.modules[module].collection,
            )
            Config.sys.conn[Config.data_name][
                Config.modules[module].collection
            ].create_index([('__deleted', 1)])

    # Test app-specific docs
    logger.debug('Testing docs')
    for doc in Config.docs:
        if not isinstance(doc, SysDoc):
            raise ConfigException('Invalid Config Attr \'docs\'')

        doc_results = await call(
            f'{doc.module}/read',
            # [TODO] Check behaviour with removed Event.ON
            # [TODO] Check behaviour with removed Event.PRE
            skip_events=[Event.PERM, Event.ATTRS_QUERY],
            env=Config.sys.env,
            query=[{doc.key: doc.key_value}],  # type: ignore
        )
        if not doc_results['args']['count']:
            skip_events = [Event.PERM]
            if doc.skip_args is True:
                skip_events.append(Event.ATTRS_DOC)
            doc.doc = cast('NawahDoc', doc.doc)
            doc_results = await call(
                f'{doc.module}/create',
                skip_events=skip_events,
                env=Config.sys.env,
                doc=doc.doc,
            )
            logger.debug(
                'App-specific doc with %s \'%s\' of module \'%s\' creation results: %s',
                doc.key,
                doc.key_value,
                doc.module,
                doc_results,
            )
            if doc_results['status'] != 200:
                raise ConfigException('Config step failed')
        Config.sys.docs[ObjectId(doc_results['args']['docs'][0]['_id'])] = SysDoc(
            module=doc.module
        )

    # Check for emulate_test mode
    if Config.emulate_test:
        Config.test = True


def _compile_anon_user():
    anon_doc = {
        '_id': ObjectId('f00000000000000000000011'),
        'name': {Config.locale: '__ANON'},
        'groups': [],
        'privileges': Config.anon_privileges,
        'locale': Config.locale,
    }
    for user_attr_name, user_attr in Config.user_attrs.items():
        if user_attr.default:
            anon_doc[user_attr_name] = copy.deepcopy(user_attr.default.value)
        else:
            anon_doc[user_attr_name] = generate_attr_val(attr_type=user_attr.type)
    for auth_attr in Config.auth_attrs:
        anon_doc[f'{auth_attr}_hash'] = Config.anon_token
    if Config.anon_doc:
        anon_doc.update(Config.anon_doc)
    return anon_doc


def _compile_anon_session():
    session_doc = {
        '_id': ObjectId('f00000000000000000000012'),
        'user': ObjectId('f00000000000000000000011'),
        'host_add': '127.0.0.1',
        'user_agent': Config.anon_token,
        'timestamp': '1970-01-01T00:00:00',
        'expiry': '1970-01-01T00:00:00',
        'token': Config.anon_token,
        'token_hash': Config.anon_token,
    }
    return session_doc
