'''Provides 'update' Base Function callable'''

import inspect
import logging
from typing import TYPE_CHECKING, Any, MutableSequence, Optional, cast

import nawah.data as Data
from nawah.config import Config
from nawah.enums import Event
from nawah.utils import call, validate_doc

from .exceptions import (DuplicateUniqueException, EmptyUpdateDocException,
                         NoDocUpdatedException, UpdateMultiUniqueException,
                         UtilityModuleDataCallException)

if TYPE_CHECKING:
    from nawah.classes import Query
    from nawah.types import NawahDoc, NawahEnv, NawahEvents, Results

logger = logging.getLogger('nawah')


async def update(
    *,
    module_name: str,
    skip_events: 'NawahEvents',
    env: 'NawahEnv',
    query: 'Query',
    doc: 'NawahDoc',
    raise_no_success: Optional[bool],
) -> 'Results':
    '''Updates docs for a module matching query 'query' '''

    module = Config.modules[module_name]

    if not module.collection:
        raise UtilityModuleDataCallException(
            module_name=module_name, func_name='update'
        )

    # Check presence and validate all attrs in doc args
    validate_doc(
        mode='update',
        doc=doc,
        attrs=module.attrs,
    )
    # Delete all attrs not belonging to the module
    shadow_doc = {}
    for attr_name in ['_id', *doc.keys()]:
        attr_root = attr_name.split('.')[0].split(':')[0]
        # Check top-level attr belong to module
        if attr_root not in module.attrs.keys():
            continue
        # Check attr is valid Doc Oper
        if (
            isinstance(doc[attr_name], dict)
            and doc[attr_name].keys()
            and list(doc[attr_name].keys())[0][0] == '$'
            and doc[attr_name][list(doc[attr_name].keys())[0]] is None
        ):
            continue
        # Add non-None attrs to shadow_doc
        if doc[attr_name] is not None:
            shadow_doc[attr_name] = doc[attr_name]

    doc = shadow_doc

    # Check if there is anything yet to update
    if not doc:
        if raise_no_success:
            raise EmptyUpdateDocException(module_name=module_name)

        return {'status': 200, 'msg': 'Nothing to update', 'args': {}}
    # Find which docs are to be updated
    docs_results = await Data.read(
        env=env,
        collection_name=module.collection,
        attrs=module.attrs,
        query=query,
        skip_process=True,
    )
    # Check unique_attrs
    if module.unique_attrs:
        # If any of the unique_attrs is present in doc, and docs_results is > 1, we have duplication
        if len(docs_results['docs']) > 1:
            unique_attrs_check = True
            for attr in module.unique_attrs:
                if isinstance(attr, str) and attr in doc:
                    unique_attrs_check = False
                    break

                if isinstance(attr, tuple):
                    for child_attr in attr:
                        if not unique_attrs_check:
                            break

                        if child_attr in doc:
                            unique_attrs_check = False
                            break

            if not unique_attrs_check:
                raise UpdateMultiUniqueException()

        # Check if any of the unique_attrs are present in doc
        if any(attr in module.unique_attrs for attr in doc):
            # Check if the doc would result in duplication after update
            unique_attrs_query: MutableSequence[Any] = [[]]
            for attr in module.unique_attrs:
                if isinstance(attr, str):
                    attr = cast(str, attr)
                    if attr in doc:
                        unique_attrs_query[0].append({attr: doc[attr]})
                elif isinstance(attr, tuple):
                    unique_attrs_query[0].append(
                        {
                            child_attr: doc[child_attr]
                            for child_attr in attr
                            if attr in doc
                        }
                    )
            unique_attrs_query.append(
                {'_id': {'$nin': [doc['_id'] for doc in docs_results['docs']]}}
            )
            unique_attrs_query.append({'$limit': 1})
            unique_results = await call(
                'base/read',
                module_name=module_name,
                skip_events=[Event.PERM],
                env=env,
                query=unique_attrs_query,
            )
            if unique_results['args']['count']:
                raise DuplicateUniqueException(unique_attrs=module.unique_attrs)

    create_diff = False
    # If module has diff enabled, and Event DIFF not skipped:
    if module.diff and Event.DIFF not in skip_events:
        create_diff = True
        # Attr Type TYPE diff, call the funcion and catch InvalidAttrException
        try:
            func_params = {
                'mode': 'create',
                'attr_name': 'diff',
                'attr_type': module.diff,
                'attr_val': None,
                'skip_events': skip_events,
                'env': env,
                'query': query,
                'doc': doc,
                'scope': doc,
            }
            await module.diff.condition(
                **{
                    param: func_params[param]
                    for param in inspect.signature(module.diff.condition).parameters
                }
            )

        except:
            # [TODO] Implement similar error logging as in retrieve_file
            create_diff = False
            logger.debug('Skipped Diff Workflow due to failed condition')

    else:
        logger.debug(
            'Skipped Diff Workflow due to: %s, %s',
            module.diff,
            Event.DIFF not in skip_events,
        )

    results = await Data.update(
        env=env,
        collection_name=module.collection,
        docs=[doc['_id'] for doc in docs_results['docs']],
        doc=doc,
    )

    if results['count'] and create_diff:
        for doc_result in docs_results['docs']:
            diff_results = await Data.create(
                env=env,
                collection_name=f'{module.collection}__diff',
                doc={
                    'user': env['session']['user']['_id'],
                    'doc': doc_result['_id'],
                    'attrs': {
                        attr.split('.')[0]: doc_result[attr.split('.')[0]]
                        for attr in doc
                    },
                },
            )
        if not diff_results['count']:
            logger.error('Failed to create Diff doc. Results: %s', diff_results)

    # update soft action is to only return the new created doc _id.
    if Event.SOFT in skip_events:
        read_results = await call(
            'base/read',
            module_name=module_name,
            skip_events=[Event.PERM],
            env=env,
            query=[{'_id': {'$in': [doc['_id'] for doc in docs_results['docs']]}}],
        )
        results = read_results['args']

    if raise_no_success is True and results['count'] == 0:
        raise NoDocUpdatedException(module_name=module_name)

    return {'status': 200, 'msg': f'Updated {results["count"]} docs', 'args': results}
