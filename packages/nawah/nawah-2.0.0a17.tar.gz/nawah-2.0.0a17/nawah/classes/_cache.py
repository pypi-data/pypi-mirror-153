'''Provides 'Cache' dataclass'''

from dataclasses import dataclass
from typing import Callable, Optional

from nawah.config import Config


@dataclass(kw_only=True)
class Cache:
    '''Cache dataclass serves role of defining Cache Instruction, which instructs Nawah of when to
    cache call results. callable for 'condition' should accept any number of following args only:
    'skip_events', 'env', 'query' '''

    channel: str
    condition: Callable
    user_scoped: bool
    period: Optional[int] = None
    file: Optional[bool] = False

    def __post_init__(self):
        Config.sys.cache_channels.add(self.channel)
