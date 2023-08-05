'''Provides 'validate_user_setting' Utility'''

from typing import TYPE_CHECKING

from nawah.classes import Attr

from ._type import validate_type

if TYPE_CHECKING:
    from nawah.classes import UserSetting

# [TODO] Use custom exceptions


def validate_user_setting(*, user_setting: 'UserSetting'):
    '''Validates attributes values of 'UserSettingDict' dict'''

    # Validate type
    if user_setting.type not in ['user', 'user_sys']:
        raise Exception(
            f'Invalid \'type\' of type \'{type(user_setting.type)}\' with required \'user\', or'
            ' \'user_sys\''
        )

    # Validate val_type
    if not isinstance(user_setting.val_type, Attr):
        raise Exception(
            f'Invalid \'val_type\' of type \'{type(user_setting.val_type)}\' with required type'
            ' \'Attr\''
        )

    # Validate val_type Attr Type
    validate_type(attr_type=user_setting.val_type)
