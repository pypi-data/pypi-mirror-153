'''Provides 'UserAttr' dataclass'''

from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ._attr import Attr
    from ._default import Default
    from ._extn import Extn
    from ._func import Func


@dataclass(kw_only=True)
class UserAttr:
    '''UserAttr dataclass serves role of defining additional 'user' module attrs, as value for
    user_attrs Config Attr. When defined, Nawah adds attr to 'user' module attrs, and adds
    privilege to module matching attr. Function of name 'update_{attr}' would be added to module
    functions, defaulting to single Permission Set with attr as privilege, allowing any user with
    'user.{attr}' in privileges to update user doc value for the attr. If 'sanitise' is True,
    'user' module 'read' function callable would remove attr from results docs'''

    type: 'Attr'
    auth_attr: bool
    sanitise: bool
    default: Optional['Default'] = None
    extn: Optional['Extn'] = None
    func: Optional['Func'] = None
