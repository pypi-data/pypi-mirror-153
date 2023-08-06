'''Provides 'setting' Nawah Core Module'''

from nawah.classes import Attr, Diff, Extn, Func, Module, Perm, Var

from ._callables import _create, _update

setting = Module(
    name='setting',
    desc='\'setting\' module module provides data type and controller for settings in Nawah '
    'eco-system. This is used by \'User\' module tp provide additional user-wise settings. It '
    'also allows for global-typed settings',
    collection='setting_docs',
    attrs={
        'user': Attr.ID(desc='\'_id\' of \'User\' doc the doc belongs to'),
        'var': Attr.STR(
            desc='Name of the setting. This is unique for every \'user\' in the module'
        ),
        'val': Attr.ANY(desc='Value of the setting'),
        'val_type': Attr.ATTR(),
        'type': Attr.LITERAL(
            desc='Type of the setting. This sets whether setting is global, or belong to user, '
            'and whether use can update it or not',
            literal=['global', 'user', 'user_sys'],
        ),
    },
    diff=Diff(condition=lambda *_: True),
    unique_attrs=[('user', 'var', 'type')],
    extns={
        'val': Extn(
            module=Var.DOC('val.__extn.module'),
            attrs=Var.DOC('val.__extn.attrs'),
            force=Var.DOC('val.__extn.force'),
        ),
    },
    funcs={
        'read': Func(
            permissions=[
                Perm(privilege='admin', query_mod={'$limit': 1}),
                Perm(
                    privilege='read',
                    query_mod={
                        'user': Var.SESSION('user'),
                        # 'type': Attr.TYPE(type=attr_query_mod_type),
                        '$limit': 1,
                    },
                ),
            ],
            query_attrs=[
                {
                    '_id': Attr.ID(),
                    'type': Attr.LITERAL(literal=['global', 'user', 'user_sys']),
                },
                {
                    'var': Attr.STR(),
                    'type': Attr.LITERAL(literal=['global']),
                },
                {
                    'var': Attr.STR(),
                    'user': Attr.ID(),
                    'type': Attr.LITERAL(literal=['user', 'user_sys']),
                },
            ],
        ),
        'create': Func(
            permissions=[
                Perm(privilege='admin'),
                Perm(privilege='create', doc_mod={'type': 'user'}),
            ],
            call_args={'raise_no_success': Attr.BOOL()},
            callable=_create,
        ),
        'update': Func(
            permissions=[
                Perm(privilege='admin', query_mod={'$limit': 1}),
                Perm(
                    privilege='update',
                    query_mod={
                        'type': 'user',
                        'user': Var.SESSION('user'),
                        '$limit': 1,
                    },
                    doc_mod={'var': None, 'val_type': None, 'type': None},
                ),
            ],
            query_attrs=[
                {
                    '_id': Attr.ID(),
                    'type': Attr.LITERAL(literal=['global', 'user', 'user_sys']),
                },
                {
                    'var': Attr.STR(),
                    'type': Attr.LITERAL(literal=['global']),
                },
                {
                    'var': Attr.STR(),
                    'user': Attr.ID(),
                    'type': Attr.LITERAL(literal=['user', 'user_sys']),
                },
            ],
            call_args={'raise_no_success': Attr.BOOL()},
            callable=_update,
        ),
        'delete': Func(
            permissions=[Perm(privilege='admin', query_mod={'$limit': 1})],
            query_attrs=[{'_id': Attr.ID()}, {'var': Attr.STR()}],
        ),
        'retrieve_file': Func(
            permissions=[Perm(privilege='*', query_mod={'type': 'global'})],
            get_func=True,
        ),
    },
)
