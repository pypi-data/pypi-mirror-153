import logging
from typing import Any, Dict

from motor.motor_asyncio import AsyncIOMotorClient

from nawah.config import Config

logger = logging.getLogger('nawah')


def create_conn() -> AsyncIOMotorClient:
    connection_config: Dict[str, Any] = {'ssl': Config.data_ssl}
    conn = AsyncIOMotorClient(Config.data_server, **connection_config, connect=True)
    return conn
