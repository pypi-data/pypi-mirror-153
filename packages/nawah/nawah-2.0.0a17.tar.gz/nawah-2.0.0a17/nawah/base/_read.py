'''Provides 'read' Base Function callable'''

import logging
from typing import TYPE_CHECKING, MutableSequence, Optional

import nawah.data as Data
from nawah.config import Config

from .exceptions import NoDocFoundException, UtilityModuleDataCallException

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahEnv, Results

logger = logging.getLogger('nawah')


async def read(
    *,
    module_name: str,
    env: 'NawahEnv',
    query: 'Query',
    raise_no_success: Optional[bool],
) -> 'Results':
    '''Reads docs from module collection that match query'''

    module = Config.modules[module_name]

    if not module.collection:
        raise UtilityModuleDataCallException(
            module_name=module_name, func_name='create'
        )

    extn_list: MutableSequence[str] = []

    extn_list = [attr_name.split('.')[0] for attr_name in module.extns]

    if '$extn' in query:
        if query['$extn'] is False:
            extn_list = []
        elif isinstance(query['$extn'], list):
            extn_list = [
                attr_name
                for attr_name in query['$extn']
                if attr_name.split(':')[0].split('.')[0] in extn_list
            ]

    if '$attrs' in query:
        extn_list = [
            attr_name for attr_name in extn_list if attr_name in query['$attrs']
        ]

    results = await Data.read(
        env=env,
        collection_name=module.collection,
        attrs=module.attrs,
        query=query,
        extn_attrs=extn_list,
    )

    # [DOC] if $attrs query arg is present return only required keys.
    if '$attrs' in query:
        query['$attrs'].insert(0, '_id')
        for i in range(len(results['docs'])):
            results['docs'][i] = {
                attr: results['docs'][i][attr]
                for attr in query['$attrs']
                if attr in results['docs'][i]
            }

    if raise_no_success is True and results['count'] == 0:
        raise NoDocFoundException(module_name=module_name)

    return {'status': 200, 'msg': f'Found {results["count"]} docs', 'args': results}
