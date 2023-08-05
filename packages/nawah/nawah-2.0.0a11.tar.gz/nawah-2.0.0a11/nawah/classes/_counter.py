'''Provides 'Counter' dataclass'''

from dataclasses import dataclass
from typing import Callable, Protocol, Union


@dataclass(kw_only=True)
class Counter:
    '''Counter dataclass serves role as Counter Value Instruction. Callable as value for 'counter'
    should accept any number of following args only: 'doc' '''

    counter: Union[str, Callable]
    pattern_formatter: 'CounterPatternFormatter'


class CounterPatternFormatter(Protocol):
    '''Provides type-hint for 'pattern_formatter' callable of 'Counter' '''

    # pylint: disable=too-few-public-methods

    def __call__(
        self,
        counter_value: int,
    ) -> str:
        ...
