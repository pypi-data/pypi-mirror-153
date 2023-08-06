'''Provides enums required for Nawah Fremework and apps'''

from enum import Enum, auto


class AttrType(Enum):
    '''Enum for all Nawah-defined Attr Types'''

    ANY = auto()
    ATTR = auto()
    ID = auto()
    STR = auto()
    INT = auto()
    FLOAT = auto()
    BOOL = auto()
    LOCALE = auto()
    LOCALES = auto()
    EMAIL = auto()
    PHONE = auto()
    IP = auto()
    URI_WEB = auto()
    DATETIME = auto()
    DATE = auto()
    TIME = auto()
    FILE = auto()
    BYTES = auto()
    GEO_POINT = auto()
    LIST = auto()
    KV_DICT = auto()
    TYPED_DICT = auto()
    LITERAL = auto()
    UNION = auto()
    TYPE = auto()


class Event(Enum):
    '''Identifies events in calls that can be skipped'''

    ATTRS_QUERY = auto()
    ATTRS_DOC = auto()
    VALIDATE = auto()
    PERM = auto()
    CACHE = auto()
    SOFT = auto()
    DIFF = auto()
    SYS_DOCS = auto()
    ANALYTICS = auto()


class DeleteStrategy(Enum):
    '''Identifies strategies of delete calls'''

    SOFT_SKIP_SYS = auto()
    SOFT_SYS = auto()
    FORCE_SKIP_SYS = auto()
    FORCE_SYS = auto()


class LocaleStrategy(Enum):
    '''Identifies strategies of values for attrs of Attr Type LOCALE'''

    DUPLICATE = auto()
    NONE_VALUE = auto()


class NawahValues(Enum):
    '''Identifies values to be used internally to pass secure values'''

    NONE_VALUE = auto()
    ALLOW_MOD = auto()


class VarType(Enum):
    '''Enum for variables types to be used with 'Var' dataclass'''

    ENV = auto()
    SESSION = auto()
    DOC = auto()
    L10N = auto()
    CONFIG = auto()
    DATE = auto()
    TIME = auto()
    DATETIME = auto()
