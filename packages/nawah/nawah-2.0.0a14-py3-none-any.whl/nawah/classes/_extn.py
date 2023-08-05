'''Provides 'Extn' dataclass'''

from dataclasses import dataclass
from typing import TYPE_CHECKING, MutableSequence, Optional, Union

if TYPE_CHECKING:
    from nawah.classes import Var
    from nawah.enums import Event
    from nawah.types import NawahQuery


@dataclass(kw_only=True)
class Extn:
    '''Extn dataclass serves role of defining Extension Instruction, which
    instructs Nawah to extend specific attr value unto another doc'''

    module: Union[str, 'Var']
    attrs: Union[MutableSequence[str], 'Var']
    force: Union[bool, str, 'Var'] = False
    skip_events: Optional[Union[MutableSequence['Event'], 'Var']] = None
    query: Optional[Union['NawahQuery', 'Var']] = None

    def __post_init__(self):
        pass
