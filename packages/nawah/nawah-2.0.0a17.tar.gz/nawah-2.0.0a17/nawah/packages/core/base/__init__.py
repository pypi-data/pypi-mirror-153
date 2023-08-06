'''Provides 'base' Nawah Core Module'''

from nawah.classes import Attr, Func, Module, Perm

base = Module(
    name='base',
    desc='\'base\' module provides necessary structure to allow modules to access Base '
    'Functions Callables via \'call\' Utility',
    funcs={
        'read': Func(
            permissions=[
                Perm(privilege='__sys'),
            ],
            call_args={'raise_no_success': Attr.BOOL()},
        ),
        'create': Func(
            permissions=[
                Perm(privilege='__sys'),
            ],
            call_args={'raise_no_success': Attr.BOOL()},
        ),
        'update': Func(
            permissions=[
                Perm(privilege='__sys'),
            ],
            call_args={'raise_no_success': Attr.BOOL()},
        ),
        'delete': Func(
            permissions=[
                Perm(privilege='__sys'),
            ],
            call_args={'raise_no_success': Attr.BOOL()},
        ),
        'obtain_lock': Func(
            permissions=[
                Perm(privilege='__sys'),
            ],
            doc_attrs={'tags': Attr.LIST(list=[Attr.STR()]), 'attempts': Attr.INT()},
        ),
        'delete_lock': Func(
            permissions=[
                Perm(privilege='__sys'),
            ],
            query_attrs={'_id': Attr.ID()},
        ),
    },
)
