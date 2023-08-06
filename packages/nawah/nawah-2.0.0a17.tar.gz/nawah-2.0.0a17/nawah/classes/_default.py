'''Provides 'Default' dataclass'''

from dataclasses import dataclass
from typing import Callable, MutableMapping, MutableSequence, Union


@dataclass(kw_only=True)
class Default:
    '''Default dataclass serves role of defining Default Instruction, which instructs Nawah to set
    value for. Callable as value for 'value' should accept any number of following args only:
    'attr_name',  'attr_type',  'attr_val',  'doc' '''

    value: Union[
        None,
        str,
        int,
        float,
        bool,
        MutableMapping,
        MutableSequence,
        Callable,
    ]

    def __post_init__(self):
        pass
