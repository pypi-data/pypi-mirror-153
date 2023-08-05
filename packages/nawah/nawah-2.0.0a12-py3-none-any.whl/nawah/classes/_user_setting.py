'''Provides 'UserSetting' dataclass, 'UserSettingDict' TypedDict'''

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal, Optional

from nawah.enums import NawahValues

if TYPE_CHECKING:
    from ._attr import Attr


@dataclass(kw_only=True)
class UserSetting:
    '''SysDoc dataclass serves role of defining 'Setting' docs that are
    required for users, as part of 'AppConfig', 'PackageConfig' '''

    type: Literal['user', 'user_sys']
    val_type: 'Attr'
    default: Optional[Any] = NawahValues.NONE_VALUE

    def __post_init__(self):
        pass
