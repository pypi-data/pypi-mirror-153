'''Provides 'delete' Data Function'''

import logging
from typing import TYPE_CHECKING, MutableSequence, Union

from bson import ObjectId

from nawah.config import Config
from nawah.enums import DeleteStrategy
from nawah.exceptions import UnknownDeleteStrategyException

if TYPE_CHECKING:
    from nawah.types import NawahEnv, ResultsArgs

logger = logging.getLogger('nawah')


async def delete(
    *,
    env: 'NawahEnv',
    collection_name: str,
    docs: MutableSequence[Union[str, ObjectId]],
    strategy: DeleteStrategy,
) -> 'ResultsArgs':
    '''Deletes 'doc' from 'collection' using connection 'conn' in 'env' '''

    # Check strategy to cherrypick update, delete calls and system_docs
    if strategy in [DeleteStrategy.SOFT_SKIP_SYS, DeleteStrategy.SOFT_SYS]:
        if strategy == DeleteStrategy.SOFT_SKIP_SYS:
            del_docs = [
                ObjectId(doc) for doc in docs if ObjectId(doc) not in Config.sys.docs
            ]
            if len(del_docs) != len(docs):
                logger.warning(
                    'Skipped soft delete for system docs due to \'DELETE_SOFT_SKIP_SYS\' strategy'
                )
        else:
            logger.warning('Detected \'DELETE_SOFT_SYS\' strategy for delete call')
            del_docs = [ObjectId(doc) for doc in docs]
        # Perform update call on matching docs
        collection = env['conn'][Config.data_name][collection_name]
        update_doc = {'$set': {'__deleted': True}}
        # If using Azure Mongo service update docs one by one
        results = await collection.update_many({'_id': {'$in': docs}}, update_doc)
        update_count = results.modified_count
        return {'count': update_count, 'docs': [{'_id': doc} for doc in docs]}

    if strategy in [DeleteStrategy.FORCE_SKIP_SYS, DeleteStrategy.FORCE_SYS]:
        if strategy == DeleteStrategy.FORCE_SKIP_SYS:
            del_docs = [
                ObjectId(doc) for doc in docs if ObjectId(doc) not in Config.sys.docs
            ]
            if len(del_docs) != len(docs):
                logger.warning(
                    'Skipped soft delete for system docs due to \'DELETE_FORCE_SKIP_SYS\' strategy'
                )
        else:
            logger.warning('Detected \'DELETE_FORCE_SYS\' strategy for delete call')
            del_docs = [ObjectId(doc) for doc in docs]
        # Perform delete query on matching docs
        collection = env['conn'][Config.data_name][collection_name]
        results = await collection.delete_many({'_id': {'$in': del_docs}})
        delete_count = results.deleted_count
        return {'count': delete_count, 'docs': [{'_id': doc} for doc in docs]}

    raise UnknownDeleteStrategyException(f'DeleteStrategy \'{strategy}\' is unknown')
