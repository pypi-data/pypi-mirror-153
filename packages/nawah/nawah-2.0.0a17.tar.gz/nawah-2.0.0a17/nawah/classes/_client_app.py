'''Provides 'ClientApp' dataclass'''

from dataclasses import dataclass
from typing import Literal, MutableSequence, Optional


@dataclass(kw_only=True)
class ClientApp:
    '''ClientApp dataclass serves role of defining item for 'client_apps' Config Attr'''

    name: str
    type: Literal['web', 'ios', 'android']
    origin: Optional[MutableSequence[str]] = None
    hash: Optional[str] = None
