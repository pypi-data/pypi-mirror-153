'''Provides 'Analytics' dataclass'''

from dataclasses import dataclass
from typing import Callable


@dataclass(kw_only=True)
class Analytics:
    '''Analytics dataclass serves role of defining an Analytics Set, which
    instructs Nawah to record analytics event for calls which 'condition'
    does not raise Exception for, formatted as 'props' '''

    condition: Callable
    props: Callable

    def __post_init__(self):
        pass
