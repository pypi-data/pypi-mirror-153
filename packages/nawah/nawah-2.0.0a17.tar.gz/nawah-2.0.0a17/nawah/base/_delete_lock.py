'''Provides 'delete_lock' Base Function callable'''

import logging
from typing import TYPE_CHECKING

import nawah.data as Data
from nawah.config import Config
from nawah.enums import DeleteStrategy

from .exceptions import FailedDeleteLockException

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahEnv, Results

logger = logging.getLogger('nawah')


async def delete_lock(
    *, module_name: str, env: 'NawahEnv', query: 'Query'
) -> 'Results':
    '''Deletes locks for a module matching query \'query\'. If not, raises MethodException.'''

    lock_id = query['_id'][0]

    module = Config.modules[module_name]

    docs_results = results = await Data.read(
        env=env,
        collection_name=f'{module.collection}__lock',
        attrs={},
        query=query,
        skip_process=True,
    )
    results = await Data.delete(
        env=env,
        collection_name=f'{module.collection}__lock',
        docs=[doc['_id'] for doc in docs_results['docs']],
        strategy=DeleteStrategy.FORCE_SYS,
    )

    if results['count'] != 1:
        logger.error(
            'Failed to delete lock \'%s\' for \'%s\'. DELETE MANUALLY NOW',
            lock_id,
            module_name,
        )
        raise FailedDeleteLockException(module_name=module_name, lock_id=lock_id)

    return {
        'status': 200,
        'msg': f'Deleted {results["count"]} docs',
        'args': results,
    }
