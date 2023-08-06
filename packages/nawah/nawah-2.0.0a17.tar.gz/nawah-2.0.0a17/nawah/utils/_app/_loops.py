import asyncio
import datetime
import logging
import sys
import time
import traceback

import aiohttp.web

from nawah.config import Config
from nawah.enums import Event

from .._call import call
from ._common_handlers import (_not_allowed_handler, _not_found_handler,
                               _root_handler)
from ._http_handler import _http_handler
from ._utils import _close_session
from ._websocket_handler import _websocket_handler

logger = logging.getLogger('nawah')


async def _jobs_loop():
    try:
        # Connection Timeout Workflow
        logger.debug('Time to check for sessions!')
        logger.debug('Current sessions: %s', Config.sys.sessions)
        for session_id, session in Config.sys.sessions.items():
            if 'last_call' not in session.keys():
                continue
            if datetime.datetime.utcnow() > (
                session['last_call'] + datetime.timedelta(seconds=Config.conn_timeout)
            ):
                logger.debug(
                    'Session #\'%s\' with REMOTE_ADDR \'%s\' HTTP_USER_AGENT: \'%s\' is idle. '
                    'Closing',
                    session['id'],
                    session['REMOTE_ADDR'],
                    session['HTTP_USER_AGENT'],
                )
                await _close_session(session_id)
    except Exception:
        logger.error('An error occurred. Details: %s', traceback.format_exc())

    try:
        # Calls Quota Workflow - Clean-up Sequence
        logger.debug('Time to check for IPs quotas!')
        del_ip_quota = []
        for ip in Config.sys.ip_quota.keys():
            if (
                datetime.datetime.utcnow() - Config.sys.ip_quota[ip]['last_check']
            ).seconds > 59:
                logger.debug(
                    f'IP \'{ip}\' with quota \'{Config.sys.ip_quota[ip]["counter"]}\' is idle. Cleaning-up'
                )
                del_ip_quota.append(ip)
        for ip in del_ip_quota:
            del Config.sys.ip_quota[ip]
    except Exception:
        logger.error(f'An error occurred. Details: {traceback.format_exc()}')

    try:
        # Jobs Workflow
        current_time = datetime.datetime.utcnow().isoformat()[:16]
        logger.debug('Time to check for jobs!')
        for job_name, job in Config.jobs.items():
            logger.debug('Checking: %s', job_name)
            if job._disabled:
                logger.debug('-Job is disabled. Skipping')
                continue
            # Check if job is scheduled for current_time
            if current_time >= job._next_time:
                logger.debug('-Job is due, running!')
                # Update job next_time
                job._next_time = datetime.datetime.fromtimestamp(
                    job._cron_schedule.get_next(), datetime.timezone.utc
                ).isoformat()[:16]

                def job_callback(task: asyncio.Future):
                    if task.done():
                        logger.debug('-Job \'%s\' is done', job_name)

                    if task_exception := task.exception():
                        logger.error('Job \'%s\' has failed with exception', job_name)
                        logger.error('Exception details:')
                        logger.error(task_exception)
                        if job.prevent_disable:
                            logger.warning(
                                '-Detected job prevent_disable. Skipping disabling job'
                            )
                        else:
                            logger.warning('-Disabling job')
                            job._disabled = True

                job_task = asyncio.create_task(job.job(env=Config.sys.env))
                job_task.add_done_callback(job_callback)

            else:
                logger.debug('-Not yet due')
    except Exception:
        logger.error(f'An error occurred. Details: {traceback.format_exc()}')

    # [TODO] Re-implement
    # try:
    #     logger.debug('Time to check for files timeout!')
    #     files_task = asyncio.create_task(
    #         call(
    #             'file/delete',
    #             skip_events=[Event.PERM],
    #             env=Config.sys.env,
    #             query=[
    #                 {
    #                     'create_time': {
    #                         '$lt': (
    #                             datetime.datetime.utcnow()
    #                             - datetime.timedelta(seconds=Config.file_upload_timeout)
    #                         ).isoformat()
    #                     }
    #                 }
    #             ],
    #         )
    #     )
    #     # logger.debug('Files timeout results:')
    #     # logger.debug('-status: %s', files_results['status'])
    #     # logger.debug('-msg: %s', files_results['msg'])
    #     # logger.debug('-args.docs: %s', files_results["args"]['docs'])
    # except Exception:
    #     logger.error('An error occurred. Details: %s', traceback.format_exc())


def _create_error_middleware(overrides):
    @aiohttp.web.middleware
    async def error_middleware(request, handler):
        try:
            response = await handler(request)
            override = overrides.get(response.status)
            if override:
                return await override(request)
            return response
        except aiohttp.web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)
            raise

    return error_middleware


async def _web_loop():
    # Populate get_routes, post_routes
    get_routes = []
    post_routes = []
    for module_name, module in Config.modules.items():
        for func_name, func in module.funcs.items():
            if func.get_func:
                for get_args_set in func.query_attrs or [{}]:
                    if get_args_set:
                        get_args = f'/{{{"}/{".join(list(get_args_set.keys()))}}}'
                    else:
                        get_args = ''

                    get_routes.append(f'/{module_name}/{func_name}{get_args}')
            elif func.post_func:
                for post_args_set in func.query_attrs or [{}]:
                    if post_args_set:
                        post_args = f'/{{{"}/{".join(list(post_args_set.keys()))}}}'
                    else:
                        post_args = ''

                    post_routes.append(f'/{module_name}/{func_name}{post_args}')

    logger.debug(
        'Loaded modules: %s',
        {module_name: module.attrs for module_name, module in Config.modules.items()},
    )
    logger.debug(
        'Config has attrs: %s',
        {
            k: str(v)
            for k, v in Config.__dict__.items()
            if not isinstance(v, classmethod) and not k.startswith('_')
        },
    )
    logger.debug('Generated get_routes: %s', get_routes)
    logger.debug('Generated post_routes: %s', post_routes)

    app = aiohttp.web.Application()
    app.middlewares.append(
        _create_error_middleware(
            {
                404: _not_found_handler,
                405: _not_allowed_handler,
            }
        )
    )
    app.router.add_route('GET', '/', _root_handler)
    app.router.add_route('*', '/ws', _websocket_handler)
    for route in get_routes:
        app.router.add_route('GET', route, _http_handler)
    for route in post_routes:
        app.router.add_route('POST', route, _http_handler)
        app.router.add_route('OPTIONS', route, _http_handler)
    logger.info('Welcome to Nawah')
    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, '0.0.0.0', Config.port)
    await site.start()
    logger.info('Serving on 0.0.0.0:%s', Config.port)
    while True:
        await asyncio.sleep(60)
        asyncio.create_task(_jobs_loop())


def _run_app():
    try:
        asyncio.run(_web_loop())
    except KeyboardInterrupt:
        if time.localtime().tm_hour >= 21 or time.localtime().tm_hour <= 4:
            msg = 'night'
        elif time.localtime().tm_hour >= 18:
            msg = 'evening'
        elif time.localtime().tm_hour >= 12:
            msg = 'afternoon'
        elif time.localtime().tm_hour >= 5:
            msg = 'morning'

        logger.info('Have a great %s!', msg)

        sys.exit()
