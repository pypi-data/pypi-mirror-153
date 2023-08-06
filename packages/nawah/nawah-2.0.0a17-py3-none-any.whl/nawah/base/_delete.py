'''Provides 'delete' Base Function callable'''

from typing import TYPE_CHECKING, Optional

import nawah.data as Data
from nawah.config import Config
from nawah.enums import DeleteStrategy, Event

from .exceptions import NoDocDeletedException, UtilityModuleDataCallException

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahEnv, NawahEvents, Results


async def delete(
    *,
    module_name: str,
    skip_events: 'NawahEvents',
    env: 'NawahEnv',
    query: 'Query',
    raise_no_success: Optional[bool],
) -> 'Results':
    '''Deletes doc from module'''

    module = Config.modules[module_name]

    if not module.collection:
        raise UtilityModuleDataCallException(
            module_name=module_name, func_name='delete'
        )

    # [TODO]: confirm all extns are not linked.
    # [DOC] Pick delete strategy based on skip_events
    strategy = DeleteStrategy.SOFT_SKIP_SYS
    if Event.SOFT not in skip_events and Event.SYS_DOCS in skip_events:
        strategy = DeleteStrategy.SOFT_SYS
    elif Event.SOFT in skip_events:
        if Event.SYS_DOCS not in skip_events:
            strategy = DeleteStrategy.FORCE_SKIP_SYS
        else:
            strategy = DeleteStrategy.FORCE_SYS

    docs_results = results = await Data.read(
        env=env,
        collection_name=module.collection,
        attrs=module.attrs,
        query=query,
        skip_process=True,
    )
    results = await Data.delete(
        env=env,
        collection_name=module.collection,
        docs=[doc['_id'] for doc in docs_results['docs']],
        strategy=strategy,
    )

    if raise_no_success is True and results['count'] == 0:
        raise NoDocDeletedException(module_name=module_name)

    return {'status': 200, 'msg': f'Deleted {results["count"]} docs', 'args': results}
