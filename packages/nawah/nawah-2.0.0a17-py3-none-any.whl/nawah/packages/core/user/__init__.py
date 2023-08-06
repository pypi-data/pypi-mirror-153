'''Provides 'user' Nawah Core Module'''

from nawah.classes import Attr, Default, Func, Module, Perm, Var

from ._callables import (_add_group, _create, _delete_group, _read,
                         _read_privileges)

user = Module(
    name='user',
    desc='\'user\' module provides data type and controller for users in Nawah eco-system. The '
    'permissions of the module methods are designed to be as secure for exposed calls, and as '
    'flexible for privileged-access',
    collection='user_docs',
    attrs={
        'name': Attr.LOCALE(desc='Name of the user as \'LOCALE\''),
        'locale': Attr.LOCALES(desc='Default locale of the user'),
        'create_time': Attr.DATETIME(
            desc='Python \'datetime\' ISO format of the doc creation'
        ),
        'login_time': Attr.DATETIME(
            desc='Python \'datetime\' ISO format of the last login'
        ),
        'groups': Attr.LIST(
            desc='List of \'_id\' for every group the user is member of',
            list=[Attr.ID(desc='\'_id\' of Group doc the user is member of')],
        ),
        'privileges': Attr.KV_DICT(
            desc='Privileges of the user. These privileges are always available to the user'
            'regardless of whether groups user is part of have them or not',
            key=Attr.STR(),
            val=Attr.LIST(list=[Attr.STR()]),
        ),
        'status': Attr.LITERAL(
            desc='Status of the user to determine whether user has access to the app or not',
            literal=['active', 'banned', 'deleted', 'disabled_password'],
        ),
    },
    defaults={
        'login_time': Default(value=None),
        'status': Default(value='active'),
        'groups': Default(value=[]),
        'privileges': Default(value={}),
    },
    funcs={
        'read': Func(
            permissions=[
                Perm(privilege='admin'),
                Perm(privilege='read', query_mod={'_id': Var.SESSION('user')}),
            ],
            call_args={
                'skip_sanitise_results': Attr.BOOL(),
            },
            callable=_read,
        ),
        'create': Func(permissions=[Perm(privilege='admin')], callable=_create),
        'update': Func(
            permissions=[
                Perm(privilege='admin', doc_mod={'groups': None}),
                Perm(
                    privilege='update',
                    query_mod={'_id': Var.SESSION('user')},
                    doc_mod={'groups': None, 'privileges': None},
                ),
            ],
            query_attrs={'_id': Attr.ID()},
        ),
        'delete': Func(
            permissions=[
                Perm(privilege='admin'),
                Perm(privilege='delete', query_mod={'_id': Var.SESSION('user')}),
            ],
            query_attrs={'_id': Attr.ID()},
        ),
        'read_privileges': Func(
            permissions=[
                Perm(privilege='admin'),
                Perm(privilege='read', query_mod={'_id': Var.SESSION('user')}),
            ],
            query_attrs={'_id': Attr.ID()},
            callable=_read_privileges,
        ),
        'add_group': Func(
            permissions=[Perm(privilege='admin')],
            query_attrs={'_id': Attr.ID()},
            doc_attrs=[{'group': Attr.ID()}, {'group': Attr.LIST(list=[Attr.ID()])}],
            callable=_add_group,
        ),
        'delete_group': Func(
            permissions=[Perm(privilege='admin')],
            query_attrs={'_id': Attr.ID(), 'group': Attr.ID()},
            callable=_delete_group,
        ),
        'retrieve_file': Func(permissions=[Perm(privilege='__sys')], get_func=True),
        'create_file': Func(permissions=[Perm(privilege='__sys')]),
        'update_file': Func(permissions=[Perm(privilege='__sys')]),
        'delete_file': Func(permissions=[Perm(privilege='__sys')]),
    },
)
