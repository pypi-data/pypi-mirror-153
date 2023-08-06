'''Provides 'Module' dataclass'''

from dataclasses import dataclass, field
from typing import (TYPE_CHECKING, Awaitable, Callable, MutableMapping,
                    MutableSequence, Optional, Tuple, Union)

if TYPE_CHECKING:
    from ._attr import Attr
    from ._counter import Counter
    from ._default import Default
    from ._diff import Diff
    from ._extn import Extn
    from ._func import Func


@dataclass(kw_only=True)
class Module:
    '''Module dataclass serves role of defining a Nawah Datatype along the
    funcs required for it. It is at the centre of Nawah, as in, any call
    in Nawah is directed to a specific Module and fulfilled by one of its
    defined funcs, completed with other configurations defined.'''

    # pylint: disable=too-many-instance-attributes

    name: str
    funcs: MutableMapping[str, 'Func']
    post_config: Optional[Callable[[], Awaitable[None]]] = None
    collection: Optional[str] = None
    desc: Optional[str] = None
    attrs: MutableMapping[str, 'Attr'] = field(default_factory=lambda: {})
    unique_attrs: MutableSequence[Union[Tuple[str, ...], str]] = field(
        default_factory=lambda: []
    )
    counters: MutableMapping[str, 'Counter'] = field(default_factory=lambda: {})
    diff: Optional['Diff'] = None
    create_draft: bool = False
    update_draft: bool = False
    defaults: MutableMapping[str, 'Default'] = field(default_factory=lambda: {})
    extns: MutableMapping[str, 'Extn'] = field(default_factory=lambda: {})
    privileges: MutableSequence[str] = field(
        default_factory=lambda: [
            'admin',
            'read',
            'create',
            'update',
            'delete',
        ]
    )
