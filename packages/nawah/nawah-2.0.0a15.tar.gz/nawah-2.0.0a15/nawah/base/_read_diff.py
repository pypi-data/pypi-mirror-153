'''Provides 'read' Base Function callable'''

from typing import TYPE_CHECKING

import nawah.data as Data
from nawah.classes import Attr
from nawah.config import Config

from .exceptions import UtilityModuleDataCallException

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahEnv, Results

DIFF_ATTRS = {
    'user': Attr.ID(),
    'doc': Attr.ID(),
    'attrs': Attr.KV_DICT(key=Attr.STR(), val=Attr.ANY()),
}


async def read_diff(
    *,
    module_name,
    env: 'NawahEnv',
    query: 'Query',
) -> 'Results':
    '''Reads diff docs for module'''

    module = Config.modules[module_name]

    if not module.collection:
        raise UtilityModuleDataCallException(
            module_name=module_name, func_name='read_diff'
        )

    results = await Data.read(
        env=env,
        collection_name=f'{module.collection}__diff',
        attrs=DIFF_ATTRS,
        query=query,
        extn_attrs=[],
    )

    return {'status': 200, 'msg': f'Found {results["count"]} docs', 'args': results}
