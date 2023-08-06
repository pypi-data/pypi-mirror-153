'''Provides 'group' Nawah Core Module'''

from nawah.classes import Attr, Default, Func, Module, Perm, Var
from nawah.config import Config

group = Module(
    name='group',
    desc='\'group\' module provides data type and controller for groups in Nawah eco-system',
    collection='group_docs',
    attrs={
        'user': Attr.ID(desc='\'_id\' of \'User\' doc the doc belongs to'),
        'name': Attr.LOCALE(desc='Name of the groups as \'LOCALE\''),
        'desc': Attr.LOCALE(
            desc='Description of the group as \'LOCALE\'. This can be used for dynamic generated '
            'groups that are meant to be exposed to end-users'
        ),
        'privileges': Attr.KV_DICT(
            desc='Privileges that any user is a member of the group has',
            key=Attr.STR(),
            val=Attr.LIST(list=[Attr.STR()]),
        ),
        'settings': Attr.KV_DICT(
            desc='\'Setting\' docs to be created, or required for members users when added to '
            'the group',
            key=Attr.STR(),
            val=Attr.ANY(),
        ),
        'create_time': Attr.DATETIME(
            desc='Python \'datetime\' ISO format of the doc creation'
        ),
    },
    defaults={
        'desc': Default(value=lambda _: {locale: '' for locale in Config.locales}),
        'privileges': Default(value={}),
        'settings': Default(value={}),
    },
    funcs={
        'read': Func(
            permissions=[
                Perm(privilege='admin'),
            ],
        ),
        'create': Func(permissions=[Perm(privilege='admin')]),
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
    },
)
