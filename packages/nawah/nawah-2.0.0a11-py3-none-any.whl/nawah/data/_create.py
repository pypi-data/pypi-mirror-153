'''Provides 'create' Data Function'''

from typing import TYPE_CHECKING

from nawah.config import Config

if TYPE_CHECKING:
    from nawah.types import NawahDoc, NawahEnv, ResultsArgs


async def create(
    *,
    env: 'NawahEnv',
    collection_name: str,
    doc: 'NawahDoc',
) -> 'ResultsArgs':
    '''Creates 'doc' in 'collection' using connection 'conn' in 'env' '''

    collection = env['conn'][Config.data_name][collection_name]
    results = await collection.insert_one(doc)
    _id = results.inserted_id
    return {'count': 1, 'docs': [{'_id': _id}]}
