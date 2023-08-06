'''Provides 'update_file' Base Function callable'''

from typing import TYPE_CHECKING

from nawah.config import Config
from nawah.enums import AttrType, Event
from nawah.exceptions import InvalidAttrException
from nawah.utils import call

from .exceptions import UtilityModuleDataCallException

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahDoc, NawahEnv, Results


async def update_file(
    *,
    module_name: str,
    env: 'NawahEnv',
    query: 'Query',
    doc: 'NawahDoc',
) -> 'Results':
    '''Updates doc with attr of list of files in module with new file'''

    module = Config.modules[module_name]

    if not module.collection:
        raise UtilityModuleDataCallException(
            module_name=module_name, func_name='update_file'
        )

    # [TODO] Allow use dot-notated attr path in attr query attr
    file_attr_name = query['attr'][0]
    if (
        file_attr_name not in module.attrs
        or module.attrs[file_attr_name].type != AttrType.LIST
        or not module.attrs[file_attr_name].args['list'][0].type != AttrType.FILE
    ):
        raise InvalidAttrException(
            attr_name=file_attr_name,
            attr_type=module.attrs[file_attr_name].type
            if file_attr_name in module.attrs
            else None,
            val_type=type(doc[file_attr_name]),
        )

    update_results = await call(
        'base/update',
        module_name=module_name,
        skip_events=[Event.PERM],
        env=env,
        query=[{'_id': query['_id'][0]}],
        doc={query['attr'][0]: {'$append': doc['file']}},
    )

    return update_results
