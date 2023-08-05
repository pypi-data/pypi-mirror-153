'''Provides 'create_file' Base Function callable'''

import datetime
import logging
from typing import TYPE_CHECKING

import nawah.data as Data
from nawah.classes import Attr
from nawah.config import Config
from nawah.enums import AttrType
from nawah.utils import extract_attr, validate_doc

from ._shared import FILE_ATTRS
from .exceptions import NoDocUpdatedException, UtilityModuleDataCallException

if TYPE_CHECKING:
    from nawah.types import NawahDoc, NawahEnv, Results

logger = logging.getLogger('nawah')


async def create_file(
    *,
    module_name: str,
    env: 'NawahEnv',
    doc: 'NawahDoc',
) -> 'Results':
    '''Creates file doc for a module'''

    module = Config.modules[module_name]

    if not module.collection:
        raise UtilityModuleDataCallException(
            module_name=module_name, func_name='create_file'
        )
    if '_id' in doc:
        return await set_file(
            module_name=module_name,
            env=env,
            doc=doc,
            raise_no_success=True,
        )

    file_attr = extract_attr(attrs=module.attrs, path=doc['attr'])

    types_pattern = None
    if file_attr.args['types']:
        types_pattern = '|'.join(file_attr.args['types'])
        # Replace astrisks (*) with dot-astrisks to mark it as valid RegExp pattern
        types_pattern = types_pattern.replace('*', '.*')

    file_doc_attrs = {
        **FILE_ATTRS,
        'file': Attr.TYPED_DICT(
            dict={
                'name': Attr.STR(),
                'lastModified': Attr.INT(),
                'type': Attr.STR(pattern=types_pattern),
                'size': Attr.INT(),
                'content': Attr(
                    desc='__sys_attr',
                    type=AttrType.BYTES,
                    args={},
                ),
            }
        ),
    }

    file_doc = {
        'user': env['session']['user']['_id'],
        'doc': '000000000000000000000000',
        'attr': doc['attr'],
        'file': {
            'name': doc['name'],
            'lastModified': doc['lastModified'],
            'type': doc['type'],
            'size': len(doc['content']),
            'content': doc['content'],
        },
        'create_time': datetime.datetime.utcnow().isoformat(),
    }

    validate_doc(mode='create', attrs=file_doc_attrs, doc=file_doc)

    # Execute Data driver create
    results = await Data.create(
        env=env, collection_name=f'{module.collection}__file', doc=file_doc
    )

    return {'status': 200, 'msg': f'Created {results["count"]} files', 'args': results}


async def set_file(
    *,
    module_name: str,
    env: 'NawahEnv',
    doc: 'NawahDoc',
    raise_no_success: bool,
) -> 'Results':
    '''Sets doc value of file created using 'create_file' '''
    module = Config.modules[module_name]

    update_results = await Data.update(
        env=env,
        collection_name=f'{module.collection}__file',
        docs=[doc['_id']],
        doc={'doc': doc['doc']},
    )

    if raise_no_success is True and update_results['count'] == 0:
        raise NoDocUpdatedException(module_name=module_name)

    return {'status': 200, 'msg': '', 'args': update_results}
