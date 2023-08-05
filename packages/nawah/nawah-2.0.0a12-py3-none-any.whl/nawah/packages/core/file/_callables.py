'''Provides 'file' Module Functions callables'''

from typing import TYPE_CHECKING

from nawah.config import Config
from nawah.enums import AttrType, Event
from nawah.exceptions import FuncException, InvalidAttrException
from nawah.utils import call, extract_attr, validate_attr

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahDoc, NawahEnv, NawahEvents, Results


async def _read(
    skip_events: 'NawahEvents', env: 'NawahEnv', query: 'Query'
) -> 'Results':
    skip_events.append(Event.PERM)
    read_results = await call(
        'base/read', module_name='file', skip_events=skip_events, env=env, query=query
    )

    if read_results['status'] != 200:
        return read_results

    for doc in read_results['args']['docs']:
        doc['file']['lastModified'] = int(doc['file']['lastModified'])

    return read_results


async def _create(env: 'NawahEnv', doc: 'NawahDoc') -> 'Results':
    if Config.file_upload_limit != -1 and len(doc['file']) > Config.file_upload_limit:
        raise FuncException(
            status=400,
            msg='File size is beyond allowed limit',
            args={
                'code': 'INVALID_SIZE',
                'attr': doc['__attr'].decode('utf-8'),
                'name': doc['name'].decode('utf-8'),
            },
        )
    if (module := doc['__module'].decode('utf-8')) not in Config.modules:
        raise FuncException(
            status=400,
            msg=f'Invalid module \'{module}\'',
            args={'code': 'INVALID_MODULE'},
        )

    try:
        attr_type = extract_attr(
            attrs=Config.modules[module].attrs,
            path=(attr := doc['__attr'].decode('utf-8')),
        )
    except (KeyError, ValueError) as e:
        raise FuncException(
            status=400,
            msg=f'Invalid attr \'{attr}\' of module \'{module}\'',
            args={'code': 'INVALID_ATTR'},
        ) from e

    doc = {
        'file': {
            'name': doc['name'].decode('utf-8'),
            'type': doc['type'].decode('utf-8'),
            'size': len(doc['file']),
            'lastModified': int(doc['lastModified'].decode('utf-8')),
            'content': doc['file'],
        },
    }
    try:
        attr_val = doc['file']
        if attr_type.type == AttrType.LIST:
            attr_val = [doc['file']]
        validate_attr(
            mode='create',
            attr_name=attr,
            attr_type=attr_type,
            attr_val=attr_val,
        )
    except InvalidAttrException as e:
        raise FuncException(
            status=400,
            msg=f'Invalid file for \'{attr}\' of module \'{module}\'',
            args={'code': 'INVALID_FILE'},
        ) from e

    create_results = await call(
        'base/create', skip_events=[Event.PERM], module_name='file', env=env, doc=doc
    )

    return create_results
