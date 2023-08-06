'''Provides 'setting' Module Functions callables'''

from typing import TYPE_CHECKING

from nawah.config import Config
from nawah.enums import Event
from nawah.exceptions import FuncException
from nawah.utils import call, decode_attr_type, validate_doc

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahDoc, NawahEnv, NawahEvents, Results


async def _create(
    env: 'NawahEnv', doc: 'NawahDoc', raise_no_success: bool
) -> 'Results':
    results = await call(
        'base/create',
        skip_events=[Event.PERM],
        module_name='setting',
        env=env,
        doc=doc,
        args={'raise_no_success': raise_no_success},
    )

    if results['status'] != 200:
        return results

    if doc['type'] in ['user', 'user_sys']:
        if (
            doc['user'] == env['session']['user']['_id']
            and doc['var'] in Config.user_doc_settings
        ):
            env['session']['user'][doc['var']] = doc['val']

    return results


async def _update(
    skip_events: 'NawahEvents',
    env: 'NawahEnv',
    query: 'Query',
    doc: 'NawahDoc',
    raise_no_success: bool,
) -> 'Results':
    for attr in doc.keys():
        if attr == 'val' or attr.startswith('val.'):
            break
    else:
        raise FuncException(
            status=400,
            msg='Could not match doc with any of the required doc_args. Failed sets: '
            '[\'val\': Missing]',
            args={'code': 'INVALID_DOC'},
        )

    setting_results = await call(
        'setting/read',
        skip_events=[Event.PERM, *skip_events],
        env=env,
        query=query,
    )
    if not setting_results['args']['count']:
        raise FuncException(
            status=400, msg='Invalid Setting doc', args={'code': 'INVALID_SETTING'}
        )

    setting = setting_results['args']['docs'][0]

    if Event.ATTRS_DOC not in skip_events:
        # [DOC] Attempt to validate val against Setting val_type
        setting_val_type = decode_attr_type(encoded_attr_type=setting['val_type'])
        validate_doc(
            mode='update',
            doc=doc,
            attrs={'val': setting_val_type},
        )

    results = await call(
        'base/update',
        skip_events=[Event.PERM],
        module_name='setting',
        env=env,
        query=query,
        doc=doc,
        args={'raise_no_success': raise_no_success},
    )

    if results['status'] != 200:
        return results

    # Safely check if type in query, as Event ATTRS_QUERY might skipped confirming its existence
    if 'type' in query and query['type'][0] in ['user', 'user_sys']:
        if (
            query['user'][0] == env['session']['user']['_id']
            and query['var'][0] in Config.user_doc_settings
        ):
            env['session']['user'][doc['var']] = doc['val']

    return results
