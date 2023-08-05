'''Provides 'Diff' dataclass'''

from dataclasses import dataclass
from typing import Callable


@dataclass(kw_only=True)
class Diff:
    '''Diff dataclass serves role of defining Diff Instruction, which defines condition for
    creating diff doc for successful update calls. Callable for 'condition' should accept any
    number of following args only: 'mode',  'attr_name',  'attr_type',  'attr_val',  'skip_events',
    'env',  'query',  'doc',  'scope' '''

    condition: Callable
