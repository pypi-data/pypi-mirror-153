import logging

from nawah.config import Config

logger = logging.getLogger('nawah')


async def _close_session(session_id: str):
    # [TODO] Check necissity to implement session_lock for deleteing env object from sessions

    if session_id not in Config.sys.sessions:
        logger.debug(f'Skipped closing session #\'{session_id}\'')
        return

    logger.debug(
        f'Closing data connection for session #\'{Config.sys.sessions[session_id]["id"]}\''
    )
    Config.sys.sessions[session_id]['conn'].close()

    logger.debug('Done closing data connection')
    logger.debug(
        f'Websocket connection status: {not Config.sys.sessions[session_id]["ws"].closed}'
    )

    if not Config.sys.sessions[session_id]['ws'].closed:
        await Config.sys.sessions[session_id]['ws'].close()
    logger.debug(f'Websocket connection for session #\'{session_id}\' closed')

    del Config.sys.sessions[session_id]
