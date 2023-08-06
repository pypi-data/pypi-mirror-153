'''Provides 'obtain_lock' Base Function callable'''

import asyncio
import logging
from typing import TYPE_CHECKING

from pymongo.errors import DuplicateKeyError

import nawah.data as Data
from nawah.classes import Query
from nawah.config import Config
from nawah.enums import DeleteStrategy

from .exceptions import FailedDeleteLockException, FailedObtainLockException

if TYPE_CHECKING:
    from nawah.types import NawahDoc, NawahEnv, Results

logger = logging.getLogger('nawah')


async def obtain_lock(
    *, module_name: str, env: 'NawahEnv', doc: 'NawahDoc'
) -> 'Results':
    '''Creates a lock for a module by creating a doc in lock collection and confirms
    it is the top lock doc. If not, deletes doc and raises 'FailedObtainLockException'.
    If deleting doc failed, raises 'FailedDeleteLockException' '''

    module = Config.modules[module_name]

    if 'total_attempts' not in doc:
        doc['total_attempts'] = doc['attempts']

    logger.debug('Attempting to obtain lock for \'%s\'', module_name)
    try:
        create_results = await Data.create(
            env=env,
            collection_name=f'{module.collection}__lock',
            doc=doc,
        )
        logger.debug(
            'Obtained intermediate lock \'%s\' for \'%s\'',
            create_results['docs'][0]['_id'],
            module_name,
        )
        read_results = await Data.read(
            env=env,
            collection_name=f'{module.collection}__lock',
            attrs={},
            query=Query(
                [
                    {'tags': {'$in': doc['tags']}} if doc['tags'] else {},
                    {'$sort': {'_id': 1}},
                ]
            ),
        )
        logger.debug('Attempting to read current lock for \'%s\'', module_name)

        if create_results['docs'][0]['_id'] == read_results['docs'][0]['_id']:
            logger.debug('Successfully obtained lock for \'%s\'', module_name)
            return {
                'status': 200,
                'msg': f'Obtained lock for \'{module_name}\'',
                'args': create_results,
            }
    except DuplicateKeyError:
        create_results = read_results = {'count': 0, 'docs': [{'_id': None}]}

    logger.warning(
        'Failed to obtain lock for \'%s\', with with created lock_id: \'%s\', but read \'%s\'',
        module_name,
        create_results['docs'][0]['_id'],
        read_results['docs'][0]['_id'],
    )

    if create_results['docs'][0]['_id']:
        logger.warning(
            'Deleting lock \'%s\', for \'%s\'',
            create_results['docs'][0]['_id'],
            module_name,
        )
        lock_delete_results = await Data.delete(
            env=env,
            collection_name=f'{module.collection}__lock',
            docs=[create_results['docs'][0]['_id']],
            strategy=DeleteStrategy.FORCE_SYS,
        )

        if lock_delete_results['count'] != 1:
            logger.error(
                'Failed to delete failed lock \'%s\' for \'%s\'. DELETE MANUALLY NOW',
                create_results['docs'][0]['_id'],
                module_name,
            )
            raise FailedDeleteLockException(
                module_name=module_name, lock_id=create_results['docs'][0]['_id']
            )

    if doc['attempts']:
        await asyncio.sleep(0.2)
        logger.warning('Reattempting to obtain lock for \'%s\'', module_name)
        doc['attempts'] -= 1
        return await obtain_lock(module_name=module_name, env=env, doc=doc)

    raise FailedObtainLockException(module_name=module_name)
