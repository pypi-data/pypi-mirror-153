'''Provides 'file' Nawah Core Module'''

from nawah.classes import Attr, Func, Module, Perm

from ._callables import _create, _read

file = Module(
    name='file',
    desc='\'file\' module provides functionality for \'File Upload Workflow\'',
    collection='file_docs',
    attrs={
        'user': Attr.ID(desc='\'_id\' of \'User\' doc file belongs to'),
        'file': Attr.FILE(desc='File object'),
        'create_time': Attr.DATETIME(
            desc='Python \'datetime\' ISO format of the doc creation'
        ),
    },
    funcs={
        'read': Func(
            permissions=[
                Perm(privilege='__sys'),
            ],
            callable=_read,
        ),
        'create': Func(
            permissions=[Perm(privilege='create')], post_func=True, callable=_create
        ),
        'delete': Func(
            permissions=[
                Perm(privilege='__sys'),
            ],
        ),
    },
)
