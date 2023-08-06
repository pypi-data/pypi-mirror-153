import copy
import logging
from typing import TYPE_CHECKING, Any, MutableMapping, MutableSequence, Union

from bson import ObjectId

from nawah.config import Config

if TYPE_CHECKING:
    from nawah.types import NawahDoc, NawahEnv, ResultsArgs

logger = logging.getLogger('nawah')


async def update(
    *,
    env: 'NawahEnv',
    collection_name: str,
    docs: MutableSequence[Union[str, ObjectId]],
    doc: 'NawahDoc',
) -> 'ResultsArgs':
    # Recreate docs list by converting all docs items to ObjectId
    docs = [ObjectId(doc) for doc in docs]
    # Perform update query on matching docs
    collection = env['conn'][Config.data_name][collection_name]
    results = None
    doc = copy.deepcopy(doc)

    # [TODO] Abstract $set pipeline with colon support for all stages

    # Prepare empty update pipeline
    update_pipeline = []

    # Iterate over attrs in doc to set update stage in pipeline
    for attr in doc.keys():
        # Prepare stage pipeline
        update_pipeline_stage_root: MutableMapping[str, Any] = {'$set': {}}
        update_pipeline_stage_current = update_pipeline_stage_root['$set']
        attr_path_part = attr
        attr_path_current = []

        if ':' in attr:
            attr_path = attr.split('.')
            for i, attr_path_part in enumerate(attr_path):
                if i == 0:
                    # First item has to have $
                    attr_path_current.append('$' + attr_path_part.split(':')[0])
                else:
                    attr_path_current.append(attr_path_part.split(':')[0])

                if ':' not in attr_path_part:
                    part_pipeline: MutableMapping[str, Any] = {
                        '$arrayToObject': {
                            '$concatArrays': [
                                {
                                    '$objectToArray': '.'.join(attr_path_current[:-1]),
                                },
                                [
                                    {
                                        'k': attr_path_part,
                                        'v': None,
                                    }
                                ],
                            ]
                        }
                    }
                    if 'v' in update_pipeline_stage_current:
                        update_pipeline_stage_current['v'] = part_pipeline
                    elif 'then' in update_pipeline_stage_current:
                        update_pipeline_stage_current['then'] = part_pipeline
                    else:
                        update_pipeline_stage_current[attr_path_part] = part_pipeline

                    update_pipeline_stage_current = part_pipeline['$arrayToObject'][
                        '$concatArrays'
                    ][1][0]
                else:
                    part_pipeline = {
                        '$map': {
                            'input': '.'.join(attr_path_current),
                            'as': f'this_{i}',
                            'in': {
                                '$cond': {
                                    'if': {
                                        '$eq': [
                                            {
                                                '$indexOfArray': [
                                                    '.'.join(attr_path_current),
                                                    f'$$this_{i}',
                                                ]
                                            },
                                            int(attr_path_part.split(':')[1]),
                                        ]
                                    },
                                    'then': None,
                                    'else': f'$$this_{i}',
                                }
                            },
                        }
                    }

                    if i != 0:
                        # For all subsequent array objects, wrap in object-to-array-to-object pipeline
                        part_pipeline = {
                            '$arrayToObject': {
                                '$concatArrays': [
                                    {
                                        '$objectToArray': '.'.join(
                                            attr_path_current[:-1]
                                        ),
                                    },
                                    [
                                        {
                                            'k': attr_path_part.split(':')[0],
                                            'v': part_pipeline,
                                        }
                                    ],
                                ]
                            }
                        }

                    if 'v' in update_pipeline_stage_current:
                        update_pipeline_stage_current['v'] = part_pipeline
                    elif 'then' in update_pipeline_stage_current:
                        update_pipeline_stage_current['then'] = part_pipeline
                    else:
                        update_pipeline_stage_current[
                            attr_path_part.split(':')[0]
                        ] = part_pipeline

                    if i == 0:
                        update_pipeline_stage_current = part_pipeline['$map']['in'][
                            '$cond'
                        ]
                    else:
                        update_pipeline_stage_current = part_pipeline['$arrayToObject'][
                            '$concatArrays'
                        ][1][0]['v']['$map']['in']['$cond']

                    attr_path_current = [f'$$this_{i}']

        # Check for $add Doc Oper
        if isinstance(doc[attr], dict) and '$add' in doc[attr]:
            add_field = (
                f'${doc[attr]["$field"]}'
                if '$field' in doc[attr].keys() and doc[attr]['$field']
                else f'${".".join(attr_path_current + [attr])}'
            )

            part_pipeline = {
                '$add': [
                    {
                        '$cond': {
                            'if': {'$not': [add_field]},
                            'then': 0,
                            'else': add_field,
                        }
                    },
                    doc[attr]['$add'],
                ]
            }

            # Add part_pipeline to update_pipeline_stage_current
            if 'v' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['v'] = part_pipeline
            elif 'then' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['then'] = part_pipeline
            else:
                update_pipeline_stage_current[attr_path_part] = part_pipeline

        # Check for $add Doc Oper
        elif isinstance(doc[attr], dict) and '$multiply' in doc[attr].keys():
            multiply_field = (
                f'${doc[attr]["$field"]}'
                if '$field' in doc[attr].keys() and doc[attr]['$field']
                else f'${".".join(attr_path_current + [attr])}'
            )

            part_pipeline = {
                '$multiply': [
                    {
                        '$cond': {
                            'if': {'$not': [multiply_field]},
                            'then': 0,
                            'else': multiply_field,
                        }
                    },
                    doc[attr]['$multiply'],
                ]
            }

            # Add part_pipeline to update_pipeline_stage_current
            if 'v' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['v'] = part_pipeline
            elif 'then' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['then'] = part_pipeline
            else:
                update_pipeline_stage_current[attr_path_part] = part_pipeline

        # Check for $append Doc Oper
        elif isinstance(doc[attr], dict) and '$append' in doc[attr].keys():
            if '$unique' not in doc[attr].keys() or doc[attr]['$unique'] is False:
                part_pipeline = {'$concatArrays': [f'${attr}', [doc[attr]['$append']]]}
            else:
                part_pipeline = {
                    '$concatArrays': [
                        f'${attr}',
                        {
                            '$cond': {
                                'if': {'$in': [doc[attr]['$append'], f'${attr}']},
                                'then': [],
                                'else': [doc[attr]['$append']],
                            }
                        },
                    ]
                }

            # Add part_pipeline to update_pipeline_stage_current
            if 'v' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['v'] = part_pipeline
            elif 'then' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['then'] = part_pipeline
            else:
                update_pipeline_stage_current[attr_path_part] = part_pipeline

        # Check for $set_index Doc Oper
        elif isinstance(doc[attr], dict) and '$set_index' in doc[attr]:
            part_pipeline = {
                '$reduce': {
                    'input': f'${attr}',
                    'initialValue': [],
                    'in': {
                        '$concatArrays': [
                            '$$value',
                            {
                                '$cond': {
                                    'if': {
                                        '$eq': [
                                            ['$$this'],
                                            [
                                                {
                                                    '$arrayElemAt': [
                                                        f'${attr}',
                                                        doc[attr]['$index'],
                                                    ]
                                                }
                                            ],
                                        ]
                                    },
                                    'then': [doc[attr]['$set_index']],
                                    'else': ['$$this'],
                                }
                            },
                        ]
                    },
                }
            }

            # Add part_pipeline to update_pipeline_stage_current
            if 'v' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['v'] = part_pipeline
            elif 'then' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['then'] = part_pipeline
            else:
                update_pipeline_stage_current[attr_path_part] = part_pipeline

        # Check for $del_val Doc Oper
        elif isinstance(doc[attr], dict) and '$del_val' in doc[attr]:
            part_pipeline = {
                '$reduce': {
                    'input': f'${attr}',
                    'initialValue': [],
                    'in': {
                        '$concatArrays': [
                            '$$value',
                            {
                                '$cond': {
                                    'if': {
                                        '$eq': [
                                            ['$$this'],
                                            doc[attr]['$del_val'],
                                        ]
                                    },
                                    'then': [],
                                    'else': ['$$this'],
                                }
                            },
                        ]
                    },
                }
            }

            # Add part_pipeline to update_pipeline_stage_current
            if 'v' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['v'] = part_pipeline
            elif 'then' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['then'] = part_pipeline
            else:
                update_pipeline_stage_current[attr_path_part] = part_pipeline

        # Check for $del_index Doc Oper
        elif isinstance(doc[attr], dict) and '$del_index' in doc[attr]:
            part_pipeline = {
                '$arrayToObject': {
                    '$reduce': {
                        'input': {
                            '$objectToArray': f'${attr}',
                        },
                        'initialValue': [],
                        'in': {
                            '$concatArrays': [
                                '$$value',
                                {
                                    '$cond': {
                                        'if': {
                                            '$eq': [
                                                '$$this.k',
                                                doc[attr]['$del_index'],
                                            ],
                                        },
                                        'then': [],
                                        'else': ['$$this'],
                                    }
                                },
                            ]
                        },
                    }
                }
            }

            # Add part_pipeline to update_pipeline_stage_current
            if 'v' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['v'] = part_pipeline
            elif 'then' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['then'] = part_pipeline
            else:
                update_pipeline_stage_current[attr_path_part] = part_pipeline

        else:
            # Add part_pipeline to update_pipeline_stage_current
            if 'v' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['v'] = {'$literal': doc[attr]}
            elif 'then' in update_pipeline_stage_current.keys():
                update_pipeline_stage_current['then'] = {'$literal': doc[attr]}
            else:
                update_pipeline_stage_current[attr_path_part] = {'$literal': doc[attr]}

        # Add stage to pipeline
        update_pipeline.append(update_pipeline_stage_root)

    logger.debug('Final update query: %s', {'_id': {'$in': docs}})
    logger.debug('Final update pipeline: %s', update_pipeline)

    results = await collection.update_many({'_id': {'$in': docs}}, update_pipeline)
    update_count = results.modified_count

    return {'count': update_count, 'docs': [{'_id': doc} for doc in docs]}
