'''Provides shared constants for Base Callables'''

from nawah.classes import Attr

FILE_ATTRS = {
    'user': Attr.ID(),
    'doc': Attr.ID(),
    'attr': Attr.STR(),
    'file': Attr.ANY(),
    'create_time': Attr.DATETIME(),
}
