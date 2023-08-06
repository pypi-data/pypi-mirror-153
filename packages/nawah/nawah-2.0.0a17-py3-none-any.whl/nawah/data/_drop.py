from typing import TYPE_CHECKING, Literal

from nawah.config import Config

if TYPE_CHECKING:
    from nawah.types import NawahEnv


async def drop(env: 'NawahEnv', collection_name: str) -> Literal[True]:
    collection = env['conn'][Config.data_name][collection_name]
    await collection.drop()
    return True
