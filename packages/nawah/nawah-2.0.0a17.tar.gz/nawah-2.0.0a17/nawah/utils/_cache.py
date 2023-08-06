'''Provieds Utilities to be used to get and set cache'''

import copy
import datetime
import inspect
import logging
from typing import TYPE_CHECKING, Any, Optional, Protocol, Tuple, cast

import jwt
import redis.exceptions

from nawah.classes import app_encoder
from nawah.config import Config

if TYPE_CHECKING:
    from nawah.classes import Cache, Func, Module, Query
    from nawah.types import NawahDoc, NawahEnv, NawahEvents, Results

logger = logging.getLogger('nawah')

Config.cache_expiry = cast(int, Config.cache_expiry)


class CacheNotConfiguredException(Exception):
    '''raises if a Cache Utility is called while app is not configured for Cache Workflow'''


class UpdateCacheRemoveCondition(Protocol):
    '''Provides type-hint for \'update_cache\' Utility \'remove_condition\' callable'''

    # pylint: disable=too-few-public-methods

    def __call__(self, *, update_doc: 'NawahDoc') -> bool:
        ...


async def check_cache_connection(attempt: int = 3):
    '''Attempts to read from cache to force re-connection if broken'''

    if not Config.sys.cache:
        raise CacheNotConfiguredException()

    try:
        await Config.sys.cache.get('__connection')
    except redis.exceptions.ConnectionError as e:
        if attempt != 0:
            return await check_cache_connection(attempt=attempt - 1)

        raise e


async def reset_cache_channel(channel: str, /):
    '''Resets specific cache `channel` by deleting it from active Redis db'''

    if not (cache := Config.sys.cache):
        raise CacheNotConfiguredException()

    await check_cache_connection()

    try:
        for key in await cache.client.keys(f'{channel}:*'):
            try:
                await cache.client.delete(key.decode('utf-8'))
            except redis.exceptions.ResponseError:
                logger.error('Failed to delete Cache Key: \'%s\'', key)
    except redis.exceptions.ConnectionError:
        logger.error(
            'Connection with Redis server \'%s\' failed. Skipping resetting Cache Channel \'%s\'.',
            Config.cache_server,
            channel,
        )


async def update_cache(
    *,
    channels: list[str],
    docs: list['ObjectId'],
    update_doc: 'NawahDoc',
    remove_condition: 'UpdateCacheRemoveCondition' = None,
):
    if not (cache := Config.sys.cache):
        raise CacheNotConfiguredException()

    remove_key = False
    try:
        if remove_condition:
            remove_key = remove_condition(update_doc=update_doc)
    except:
        remove_key = True

    for channel in channels:

        if channel.endswith(':'):
            channel += '*'
        elif not channel.endswith(':*'):
            channel += ':*'

        try:
            await check_cache_connection()

            for key in await cache.client.keys(channel):
                key = key.decode('utf-8')

                key_docs = await cache.get(key, '.docs')
                for doc in docs:
                    try:
                        doc_index = key_docs.index(str(doc))
                    except ValueError:
                        continue
                    if remove_key:
                        try:
                            await cache.delete(key, '.')
                        except redis.exceptions.ResponseError:
                            logger.error(
                                'Cache command failed with \'ResponseError\'. Current scope:'
                            )
                            logger.error(locals())
                        continue
                    if await cache.get(
                        key, f'.results.args.docs[{doc_index}]._id'
                    ) != str(doc):
                        try:
                            await cache.delete(key, '.')
                        except redis.exceptions.ResponseError as e:
                            logger.error(
                                'Cache command failed with \'ResponseError\': \'%s\'',
                                e,
                            )
                            logger.error('Current scope: %s', locals())
                    try:
                        for attr_name in update_doc:
                            if update_doc[attr_name] == None:
                                continue
                            await cache.set(
                                key,
                                f'.results.args.docs[{doc_index}].{attr_name}',
                                update_doc[attr_name],
                            )
                    except redis.exceptions.ResponseError as e:
                        logger.error(
                            'Cache command failed with \'ResponseError\': \'%s\'',
                            e,
                        )
                        logger.error('Current scope: %s', locals())
                        logger.error(
                            'Removing key \'%s\' due to failed update attempt.', key
                        )
                        try:
                            await cache.delete(key, '.')
                        except redis.exceptions.ResponseError as e:
                            logger.error(
                                'Cache command failed with \'ResponseError\': \'%s\'',
                                e,
                            )
                            logger.error('Current scope: %s', locals())
                try:
                    await cache.set(
                        key,
                        '.results.args.cache_time',
                        datetime.datetime.utcnow().isoformat(),
                    )
                except redis.exceptions.ResponseError as e:
                    logger.error(
                        'Cache command failed with \'ResponseError\': \'%s\'',
                        e,
                    )
                    logger.error('Current scope: %s', locals())
        except redis.exceptions.ConnectionError:
            logger.error(
                'Connection with Redis server \'%s\' failed. Skipping updating Cache Channel \'%s\'.',
                Config.cache_server,
                channel,
            )


def _generate_cache_key(
    *,
    func: 'Func',
    skip_events: 'NawahEvents',
    env: 'NawahEnv',
    query: 'Query',
) -> Optional[str]:
    if not Config.sys.cache or not func.cache:
        return None

    condition_params = {
        'skip_events': skip_events,
        'env': env,
        'query': query,
    }

    if not func.cache.condition(
        **{
            param: condition_params[param]
            for param in inspect.signature(func.cache.condition).parameters
        }
    ):
        return None

    cache_key = {
        'query': app_encoder.encode(query._query),
        'special': app_encoder.encode(query._special),
        'user': env['session']['user']['_id'] if func.cache.user_scoped else None,
    }

    cache_key_jwt = jwt.encode(cache_key, '_').split('.')[1]

    return cache_key_jwt


async def _call_cache(func: 'Func', cache_key: str):
    if not Config.sys.cache:
        return

    module = cast('Module', func.module)
    cache = cast('Cache', func.cache)

    try:
        logger.debug(
            'Attempting to get cache with \'key\': \'%s\'.',
            f'.{module.name}.{func.name}.{cache_key}',
        )

        await check_cache_connection()

        if cache.file:
            cache_dict = None
            file_cache = await Config.sys.cache.client.hgetall(
                f'__files__:{cache.channel}:{module.name}:{func.name}:{cache_key}',
            )
            if file_cache:
                cache_dict = {
                    'status': 200,
                    'msg': '',
                    'args': {
                        'return': 'file',
                        'docs': [
                            {
                                file_cache_key.decode('utf-8'): file_cache_val
                                if file_cache_key == b'content'
                                else file_cache_val.decode('utf-8')
                                for file_cache_key, file_cache_val in file_cache.items()
                            }
                        ],
                    },
                }

        else:
            cache_dict = await Config.sys.cache.get(
                f'{cache.channel}:{module.name}:{func.name}:{cache_key}',
                '.results',
            )

        return cache_dict

    except redis.exceptions.ResponseError:
        return

    except redis.exceptions.ConnectionError:
        logger.error(
            'Connection with Redis server \'%s\' failed. Skipping Cache Workflow.',
            Config.cache_server,
        )
        return


async def _set_cache(*, func: 'Func', cache_key: str, results: 'Results'):
    if not Config.sys.cache:
        return

    module = cast('Module', func.module)
    cache = cast('Cache', func.cache)

    cache_key_long = f'{cache.channel}:{module.name}:{func.name}:{cache_key}'
    results = copy.deepcopy(results)

    try:
        logger.debug(
            'Attempting to set cache with \'key\': \'%s\'.',
            cache_key_long,
        )

        await check_cache_connection()

        cache_dict = {
            'docs': [doc['_id'] for doc in results['args']['docs']]
            if 'args' in results and 'docs' in results['args']
            else [],
            'results': results,
        }

        # Check if results contain file, and set using regular Redis cache
        if cache.file:
            # Update value for cache_key_long to prevent conflict with RedisJSON cache
            cache_key_long = f'__files__:{cache_key_long}'
            # Set cache
            await Config.sys.cache.client.hset(
                cache_key_long,
                mapping=results['args']['docs'][0],
            )

        # Otherwise, set as RedisJSON cache
        else:
            await Config.sys.cache.set(
                cache_key_long,
                '.',
                app_encoder.encode(cache_dict),
            )

        if Config.cache_expiry:
            await Config.sys.cache.client.expire(
                cache_key_long,
                Config.cache_expiry,
            )

    except redis.exceptions.ConnectionError:
        logger.error(
            'Connection with Redis server \'%s\' failed. Skipping Cache Workflow.',
            Config.cache_server,
        )


async def _get_cache(
    *,
    func: 'Func',
    skip_events: 'NawahEvents',
    env: 'NawahEnv',
    query: 'Query',
) -> Tuple[Optional[str], Any]:
    cache_key = _generate_cache_key(
        func=func,
        skip_events=skip_events,
        env=env,
        query=query,
    )
    call_cache = None

    if not cache_key:
        return (None, None)

    call_cache = await _call_cache(func=func, cache_key=cache_key)

    return (cache_key, call_cache)
