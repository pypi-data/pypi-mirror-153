'''Provides 'core' Nawah Package'''

from nawah.classes import Package

from .base import base
from .group import group
from .session import session
from .setting import setting
from .user import user

core = Package(
    name='core',
    api_level='2.0',
    version='2.0.0',
    modules=[base, user, group, session, setting],
)
