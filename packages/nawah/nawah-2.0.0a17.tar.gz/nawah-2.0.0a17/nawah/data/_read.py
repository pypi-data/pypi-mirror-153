import copy
import logging
from typing import (TYPE_CHECKING, Any, MutableMapping, MutableSequence,
                    Optional, Union, cast)

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from nawah.classes import Var
from nawah.config import Config
from nawah.enums import AttrType, Event, LocaleStrategy

from ._query import _compile_query

if TYPE_CHECKING:
    from nawah.classes import Attr, Extn, Query
    from nawah.types import NawahDoc, NawahEnv, NawahQuery

logger = logging.getLogger('nawah')


async def read(
    *,
    env: 'NawahEnv',
    collection_name: str,
    attrs: MutableMapping[str, 'Attr'],
    query: 'Query',
    skip_process: bool = False,
    extn_attrs: MutableSequence[str] = [],
) -> MutableMapping[str, Any]:
    skip, limit, sort, group, aggregate_query = _compile_query(
        collection_name=collection_name, attrs=attrs, query=query
    )

    logger.debug(f'aggregate_query: {aggregate_query}')
    logger.debug(f'skip, limit, sort, group: {skip}, {limit}, {sort}, {group}.')

    collection: AsyncIOMotorCollection = env['conn'][Config.data_name][collection_name]
    docs_total_results = collection.aggregate(
        aggregate_query + [{'$count': '__docs_total'}],
        allowDiskUse=Config.data_disk_use,
    )
    try:
        async for doc in docs_total_results:
            docs_total = doc['__docs_total']
        docs_total
    except:
        return {'total': 0, 'count': 0, 'docs': [], 'groups': []}

    groups = {}
    if group:
        for group_condition in group:
            group_query = aggregate_query + [
                {
                    '$bucketAuto': {
                        'groupBy': '$' + group_condition['by'],
                        'buckets': group_condition['count'],
                    }
                }
            ]
            check_group = False
            for i in range(len(group_query)):
                if (
                    list(group_query[i].keys())[0] == '$match'
                    and list(group_query[i]['$match'].keys())[0]
                    == group_condition['by']
                ):
                    check_group = True
                    break
            if check_group:
                del group_query[i]
            group_query_results = collection.aggregate(
                group_query, allowDiskUse=Config.data_disk_use
            )
            groups[group_condition['by']] = [
                {
                    'min': group['_id']['min'],
                    'max': group['_id']['max'],
                    'count': group['count'],
                }
                async for group in group_query_results
            ]

    if sort is not None:
        aggregate_query.append({'$sort': sort})
    if skip is not None:
        aggregate_query.append({'$skip': skip})
    if limit is not None:
        aggregate_query.append({'$limit': limit})

    logger.debug(f'final query: {collection}, {aggregate_query}.')

    docs_count_results = collection.aggregate(
        aggregate_query + [{'$count': '__docs_count'}],
        allowDiskUse=Config.data_disk_use,
    )
    try:
        async for doc in docs_count_results:
            docs_count = doc['__docs_count']
        docs_count
    except:
        return {
            'total': docs_total,
            'count': 0,
            'docs': [],
            'groups': {} if not group else groups,
        }
    docs = collection.aggregate(aggregate_query, allowDiskUse=Config.data_disk_use)
    models = []
    extn_models: MutableMapping[str, Optional[MutableMapping]] = {}
    async for doc in docs:
        if not skip_process:
            doc = await _process_results_doc(
                env=env,
                attrs=attrs,
                doc=doc,
                extn_models=extn_models,
                extn_attrs=extn_attrs,
            )
        if doc:
            models.append(doc)
    return {
        'total': docs_total,
        'count': docs_count,
        'docs': models,
        'groups': {} if not group else groups,
    }


async def _process_results_doc(
    *,
    env: 'NawahEnv',
    attrs: MutableMapping[str, 'Attr'],
    doc: 'NawahDoc',
    extn_models: MutableMapping[str, Optional[MutableMapping]],
    extn_attrs: MutableSequence[str],
) -> MutableMapping[str, Any]:
    # Process doc attrs
    for attr in attrs.keys():
        if attrs[attr].type == AttrType.LOCALE:
            if (
                attr in doc.keys()
                and isinstance(doc[attr], dict)
                and Config.locale in doc[attr].keys()
            ):
                if Config.locale_strategy == LocaleStrategy.NONE_VALUE:
                    doc[attr] = {
                        locale: doc[attr][locale]
                        if locale in doc[attr].keys()
                        else None
                        for locale in Config.locales
                    }
                elif callable(Config.locale_strategy):
                    doc[attr] = {
                        locale: doc[attr][locale]
                        if locale in doc[attr].keys()
                        else Config.locale_strategy(
                            attr_val=doc[attr][Config.locale], locale=locale
                        )
                        for locale in Config.locales
                    }
                else:
                    doc[attr] = {
                        locale: doc[attr][locale]
                        if locale in doc[attr].keys()
                        else doc[attr][Config.locale]
                        for locale in Config.locales
                    }

        if attr not in extn_attrs:
            continue

        await _extend_attr(
            doc=doc,
            scope=doc,
            attr_name=attr,
            attr_type=attrs[attr],
            env=env,
            extn_models=extn_models,
        )
    # Attempt to extned the doc per extns
    return doc


async def _extend_attr(
    *,
    doc: 'NawahDoc',
    scope: Union[MutableMapping[str, Any], MutableSequence[Any]],
    attr_name: Union[str, int],
    attr_type: 'Attr',
    env: 'NawahEnv',
    extn_models: MutableMapping[str, Optional[MutableMapping]],
):
    # If scope is missing attr_name skip
    if isinstance(scope, dict) and attr_name not in scope:
        return

    # Check attr_type for possible types that require deep checking for extending
    if attr_type.type == AttrType.KV_DICT:
        attr_name = cast(str, attr_name)
        scope = cast(MutableMapping[str, Any], scope)
        if scope[attr_name] and isinstance(scope[attr_name], dict):
            for child_attr in scope[attr_name]:
                # attr_type is KV_DICT where Attr Type Arg val could be extended
                await _extend_attr(
                    doc=doc,
                    scope=scope[attr_name],
                    attr_name=child_attr,
                    attr_type=attr_type.args['val'],
                    env=env,
                    extn_models=extn_models,
                )
    if attr_type.type == AttrType.TYPED_DICT:
        attr_name = cast(str, attr_name)
        scope = cast(MutableMapping[str, Any], scope)
        if scope[attr_name] and isinstance(scope[attr_name], dict):
            for child_attr in attr_type.args['dict']:
                # attr_type is TYPED_DICT where each dict item could be extended
                await _extend_attr(
                    doc=doc,
                    scope=scope[attr_name],
                    attr_name=child_attr,
                    attr_type=attr_type.args['dict'][child_attr],
                    env=env,
                    extn_models=extn_models,
                )

    elif attr_type.type == AttrType.LIST:
        attr_name = cast(str, attr_name)
        scope = cast(MutableMapping[str, Any], scope)
        if scope[attr_name] and isinstance(scope[attr_name], list):
            for child_attr in attr_type.args['list']:
                # attr_type is LIST where it could have KV_DICT, TYPED_DICT, ID Attrs Types that can be [deep-]extended
                if child_attr.type == AttrType.KV_DICT:
                    for child_scope in scope[attr_name]:
                        if isinstance(child_scope, dict):
                            for child_child_attr in child_scope:
                                await _extend_attr(
                                    doc=doc,
                                    scope=child_scope,
                                    attr_name=child_child_attr,
                                    attr_type=child_attr.args['val'],
                                    env=env,
                                    extn_models=extn_models,
                                )
                elif child_attr.type == AttrType.TYPED_DICT:
                    for child_scope in scope[attr_name]:
                        if isinstance(child_scope, dict):
                            for child_child_attr in child_attr.args['dict']:
                                await _extend_attr(
                                    doc=doc,
                                    scope=child_scope,
                                    attr_name=child_child_attr,
                                    attr_type=child_attr.args['dict'][child_child_attr],
                                    env=env,
                                    extn_models=extn_models,
                                )
                elif child_attr.type == AttrType.ID:
                    for i in range(len(scope[attr_name])):
                        await _extend_attr(
                            doc=doc,
                            scope=scope[attr_name],
                            attr_name=i,
                            attr_type=child_attr,
                            env=env,
                            extn_models=extn_models,
                        )

    if not attr_type.extn:
        return

    attr_name = cast(str, attr_name)
    scope = cast(MutableMapping[str, Any], scope)
    # Attr is having Extn for _extn value, attempt to extend attr based on scope type
    if isinstance(scope[attr_name], str):
        try:
            scope[attr_name] = await _extend_doc(
                env=env,
                doc=doc,
                attr=scope[attr_name],
                extn_id=scope[attr_name],
                extn=attr_type.extn,
                extn_models=extn_models,
            )
        except Exception as e:
            pass

    elif isinstance(scope[attr_name], list):
        for i, extn_id in enumerate(scope[attr_name]):
            scope[attr_name][i] = await _extend_doc(
                env=env,
                doc=doc,
                attr=scope[attr_name],
                extn_id=extn_id,
                extn=attr_type.extn,
                extn_models=extn_models,
            )


async def _extend_doc(
    *,
    env: 'NawahEnv',
    doc: 'NawahDoc',
    attr: Optional['NawahDoc'],
    extn_id: str,
    extn: 'Extn',
    extn_models: MutableMapping[str, Optional[MutableMapping]],
) -> Optional[MutableMapping]:
    from nawah.utils import call, var_value

    extn_module_name: str
    # Check if extn module is dynamic value
    if isinstance(extn.module, Var):
        extn_module_name = var_value(extn.module, env=env, doc=doc)
    else:
        extn_module_name = extn.module
    extn_module = Config.modules[extn_module_name]
    # Check if extn attr set to fetch all or specific attrs
    if isinstance(extn.attrs, Var):
        extn_attrs = var_value(extn.attrs, env=env, doc=doc)
        if extn_attrs[0] == '*':
            extn_attrs = list(extn_module.attrs)
    elif extn.attrs[0] == '*':
        extn_attrs = list(extn_module.attrs)
    else:
        extn_attrs = copy.deepcopy(extn.attrs)
    # Implicitly add _id key to extn attrs so that we don't delete it in process
    if '_id' not in extn_attrs:
        extn_attrs.append('_id')
    # Set skip events
    skip_events = [Event.PERM]
    # Check value for Extn.skip_events
    if isinstance(extn.skip_events, list):
        skip_events.extend(extn.skip_events)
    elif isinstance(extn.skip_events, Var):
        skip_events.extend(var_value(extn.skip_events, env=env, doc=doc))
    # Check if extn instruction is explicitly requires second-dimension extn.
    extn_extns = []
    extn_force = False
    if isinstance(extn.force, Var):
        extn_force = var_value(extn.force, env=env, doc=doc)
    if extn.force is True:
        extn_force = True
    if extn_force:
        extn_extns = extn_attrs
    extn_query: 'NawahQuery' = [{'_id': ObjectId(extn_id)}, {'$extn': extn_extns}]
    # Check if additional query steps are to be appended
    # Read doc if not in extn_models
    extn_model_key = str(extn_id) + '_extn_' + str(extn_extns)
    if extn_model_key not in extn_models.keys():
        extn_results = await call(
            f'{extn_module_name}/read',
            skip_events=skip_events,
            env=env,
            query=extn_query,
        )
        if extn_results['args']['count']:
            extn_models[extn_model_key] = extn_results['args']['docs'][0]
        else:
            extn_models[extn_model_key] = None
    # Set attr to extn_models doc
    extn_doc = copy.deepcopy(extn_models[extn_model_key])
    # delete all unneeded keys from the resulted doc
    if extn_doc:
        extn_doc = {attr: extn_doc[attr] for attr in extn_attrs if attr in extn_doc}
    return extn_doc
