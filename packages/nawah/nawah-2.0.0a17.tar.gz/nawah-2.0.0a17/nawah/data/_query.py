import copy
import logging
import re
from typing import (TYPE_CHECKING, Any, MutableMapping, MutableSequence,
                    Optional, Tuple, Union, cast)

from bson import ObjectId

from nawah.classes import Query
from nawah.config import Config
from nawah.enums import AttrType

if TYPE_CHECKING:
    from nawah.classes import Attr
    from nawah.types import NawahQuerySpecialGroup

logger = logging.getLogger('nawah')


def _compile_query(
    *,
    collection_name: str,
    attrs: MutableMapping[str, 'Attr'],
    query: Query,
) -> Tuple[
    Optional[int],
    Optional[int],
    MutableMapping[str, int],
    Optional[MutableSequence['NawahQuerySpecialGroup']],
    MutableSequence[Any],
]:
    aggregate_prefix: MutableSequence[Any] = []
    aggregate_suffix: MutableSequence[Any] = []
    aggregate_query: MutableSequence[Any] = [{'$match': {'$and': []}}]
    aggregate_match = aggregate_query[0]['$match']['$and']
    skip: Optional[int] = None
    limit: Optional[int] = None
    sort: MutableMapping[str, int] = {'_id': -1}
    group: Optional[MutableSequence['NawahQuerySpecialGroup']] = None
    logger.debug('attempting to process query: %s', query)

    query = copy.deepcopy(query)

    # Convert all values to _id attrs to ObjectId
    # for i in range(len(query['_id'])):
    #     query['_id'][i] = ObjectId(query['_id'][i])

    # for oper in ['ne', 'gt', 'gte', 'lt', 'lte']:
    #     for i in range(len(query[f'_id:${oper}'])):
    #         query[f'_id:${oper}'][i] = ObjectId(query[f'_id:${oper}'][i][f'${oper}'])

    # for oper in ['in', 'nin']:
    #     for i in range(len(query[f'_id:${oper}'])):
    #         query[f'_id:${oper}'][i] = [
    #             ObjectId(_id) for _id in query[f'_id:${oper}'][i][f'${oper}']
    #         ]

    # [DOC] Update variables per Doc Mode
    if '__deleted' not in query or query['__deleted'] is False:
        aggregate_prefix.append({'$match': {'__deleted': {'$exists': False}}})
    else:
        # [DOC] This condition is expanded to allow __deleted = True, __deleted = None to have del query[__deleted] be applied to both conditions
        if query['__deleted'][0] is True:
            aggregate_prefix.append({'$match': {'__deleted': {'$exists': True}}})
        del query['__deleted'][0]

    if '__create_draft' not in query or query['__create_draft'] is False:
        aggregate_prefix.append({'$match': {'__create_draft': {'$exists': False}}})
    else:
        if query['__create_draft'][0] is True:
            aggregate_prefix.append({'$match': {'__create_draft': {'$exists': True}}})
        del query['__create_draft'][0]

    if ('__update_draft' not in query and '__update_draft:$ne' not in query) or query[
        '__update_draft'
    ] is False:
        query_update_draft = False
        aggregate_prefix.append({'$match': {'__update_draft': {'$exists': False}}})
    else:
        query_update_draft = True
        aggregate_prefix.append({'$match': {'__update_draft': {'$exists': True}}})
        if '__update_draft' in query and isinstance(
            query['__update_draft'][0], ObjectId
        ):
            aggregate_prefix.append(
                {'$match': {'__update_draft': query['__update_draft'][0]}}
            )
        elif '__update_draft:$ne' in query and query['__update_draft:$ne'][0] is False:
            aggregate_prefix.append({'$match': {'__update_draft': {'$ne': False}}})
        try:
            del query['__update_draft'][0]
        except:
            del query['__update_draft:$ne'][0]

    # [DOC] Update variables per Query Special Args
    if '$skip' in query:
        skip = query['$skip']
        del query['$skip']
    if '$limit' in query:
        limit = query['$limit']
        del query['$limit']
    if '$sort' in query:
        sort = query['$sort']
        del query['$sort']
    if '$group' in query:
        group = query['$group']
        del query['$group']
    if '$search' in query:
        aggregate_prefix.insert(0, {'$match': {'$text': {'$search': query['$search']}}})
        project_query: MutableMapping[str, Any] = {
            attr: '$' + attr for attr in attrs.keys()
        }
        project_query['_id'] = '$_id'
        project_query['__score'] = {'$meta': 'textScore'}
        aggregate_suffix.append({'$project': project_query})
        aggregate_suffix.append({'$match': {'__score': {'$gt': 0.5}}})
        del query['$search']
    if '$geo_near' in query:
        aggregate_prefix.insert(
            0,
            {
                '$geoNear': {
                    'near': {
                        'type': 'Point',
                        'coordinates': query['$geo_near']['val'],
                    },
                    'distanceField': query['$geo_near']['attr'] + '.__distance',
                    'maxDistance': query['$geo_near']['dist'],
                    'spherical': True,
                }
            },
        )
        del query['$geo_near']

    for step in query:
        _compile_query_step(
            aggregate_prefix=aggregate_prefix,
            aggregate_suffix=aggregate_suffix,
            aggregate_match=aggregate_match,
            collection_name=collection_name,
            attrs=attrs,
            step=step,
        )

    if '$attrs' in query and type(query['$attrs']) == list:
        group_query = {
            '_id': '$_id',
            **{
                attr: {'$first': f'${attr}'}
                for attr in query['$attrs']
                if attr in attrs.keys()
            },
        }
        # [DOC] We need to expose __update_draft value if it is queried as this refers to the original doc to be updated
        if query_update_draft:
            group_query['__update_draft'] = {'$first': '$__update_draft'}
        aggregate_suffix.append({'$group': group_query})
    else:
        group_query = {
            '_id': '$_id',
            **{attr: {'$first': f'${attr}'} for attr in attrs.keys()},
        }
        # [DOC] We need to expose __update_draft value if it is queried as this refers to the original doc to be updated
        if query_update_draft:
            group_query['__update_draft'] = {'$first': '$__update_draft'}
        aggregate_suffix.append({'$group': group_query})

    logger.debug(
        f'processed query, aggregate_prefix:{aggregate_prefix}, aggregate_suffix:{aggregate_suffix}, aggregate_match:{aggregate_match}'
    )
    if len(aggregate_match) == 1:
        aggregate_query = [{'$match': aggregate_match[0]}]
    elif len(aggregate_match) == 0:
        aggregate_query = []

    aggregate_query = aggregate_prefix + aggregate_query + aggregate_suffix
    return (skip, limit, sort, group, aggregate_query)


def _compile_query_step(
    *,
    aggregate_prefix: MutableSequence[Any],
    aggregate_suffix: MutableSequence[Any],
    aggregate_match: MutableSequence[Any],
    collection_name: str,
    attrs: MutableMapping[str, 'Attr'],
    step: Union[MutableMapping[str, Any], MutableSequence[Any]],
) -> None:
    if type(step) == dict and len(step.keys()):  # type: ignore
        step = cast(MutableMapping[str, Any], step)
        child_aggregate_query: MutableMapping[str, Any] = {'$and': []}
        for attr in step.keys():
            if attr.startswith('__or'):
                child_child_aggregate_query: MutableMapping[str, Any] = {'$or': []}
                _compile_query_step(
                    aggregate_prefix=aggregate_prefix,
                    aggregate_suffix=aggregate_suffix,
                    aggregate_match=child_child_aggregate_query['$or'],
                    collection_name=collection_name,
                    attrs=attrs,
                    step=step[attr],
                )
                if len(child_child_aggregate_query['$or']) == 1:
                    child_aggregate_query['$and'].append(
                        child_child_aggregate_query['$or'][0]
                    )
                elif len(child_child_aggregate_query['$or']) > 1:
                    child_aggregate_query['$and'].append(
                        child_child_aggregate_query['$or']
                    )
            else:
                # [DOC] Add extn query when required
                if (
                    attr.find('.') != -1
                    and attr.split('.')[0] in attrs.keys()
                    and attrs[attr.split('.')[0]].extn
                ):
                    # [TODO] Check if this works with EXTN as Attr Type TYPE
                    step_attr = attr.split('.')[1]
                    step_attrs: MutableMapping[str, 'Attr'] = Config.modules[
                        attrs[attr.split('.')[0]].extn.module
                    ].attrs

                    # [DOC] Don't attempt to extn attr that is already extended
                    lookup_query = False
                    for stage in aggregate_prefix:
                        if (
                            '$lookup' in stage.keys()
                            and stage['$lookup']['as'] == attr.split('.')[0]
                        ):
                            lookup_query = True
                            break
                    if not lookup_query:
                        extn_collection = Config.modules[
                            attrs[attr.split('.')[0]].extn.module
                        ].collection
                        aggregate_prefix.append(
                            {
                                '$addFields': {
                                    attr.split('.')[0]: {
                                        '$toObjectId': f'${attr.split(".")[0]}'
                                    }
                                }
                            }
                        )
                        aggregate_prefix.append(
                            {
                                '$lookup': {
                                    'from': extn_collection,
                                    'localField': attr.split('.')[0],
                                    'foreignField': '_id',
                                    'as': attr.split('.')[0],
                                }
                            }
                        )
                        aggregate_prefix.append({'$unwind': f'${attr.split(".")[0]}'})
                        group_query: MutableMapping[str, Any] = {
                            attr: {'$first': f'${attr}'} for attr in attrs.keys()
                        }
                        group_query[attr.split('.')[0]] = {
                            '$first': f'${attr.split(".")[0]}._id'
                        }
                        group_query['_id'] = '$_id'
                        aggregate_suffix.append({'$group': group_query})
                else:
                    step_attr = attr
                    step_attrs = attrs

                # [DOC] Convert strings and lists of strings to ObjectId when required
                if step_attr == '_id':
                    try:
                        if isinstance(step[attr], str):
                            step[attr] = ObjectId(step[attr])
                        elif isinstance(step[attr], list):
                            step[attr] = [
                                ObjectId(child_attr) for child_attr in step[attr]
                            ]
                        elif (
                            isinstance(step[attr], dict) and '$in' in step[attr].keys()
                        ):
                            step[attr] = {
                                '$in': [
                                    ObjectId(child_attr)
                                    for child_attr in step[attr]['$in']
                                ]
                            }
                    except:
                        logger.warning(
                            f'Failed to convert attr to id type: {step[attr]}'
                        )
                # [DOC] Check for query oper
                if type(step[attr]) == dict:
                    if '$regex' in step[attr].keys():
                        step[attr] = {
                            '$regex': re.compile(
                                step[attr]['$regex'], re.RegexFlag.IGNORECASE
                            )
                        }

                if type(step[attr]) == dict and '$match' in step[attr].keys():
                    child_aggregate_query['$and'].append(step[attr]['$match'])
                else:
                    child_aggregate_query['$and'].append({attr: step[attr]})
        if len(child_aggregate_query['$and']) == 1:
            aggregate_match.append(child_aggregate_query['$and'][0])
        elif len(child_aggregate_query['$and']) > 1:
            aggregate_match.append(child_aggregate_query)
    elif type(step) == list and len(step):
        step = cast(MutableSequence[Any], step)
        child_aggregate_query = {'$or': []}
        for child_step in step:
            _compile_query_step(
                aggregate_prefix=aggregate_prefix,
                aggregate_suffix=aggregate_suffix,
                aggregate_match=child_aggregate_query['$or'],
                collection_name=collection_name,
                attrs=attrs,
                step=child_step,
            )
        if len(child_aggregate_query['$or']) == 1:
            aggregate_match.append(child_aggregate_query['$or'][0])
        elif len(child_aggregate_query['$or']) > 1:
            aggregate_match.append(child_aggregate_query)
