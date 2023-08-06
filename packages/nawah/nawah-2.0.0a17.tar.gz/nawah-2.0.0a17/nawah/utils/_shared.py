'''Shared items required by multiple Utilities'''

from math import inf
from typing import Literal, MutableMapping, MutableSequence, TypedDict


class AttrTypeArgValidation(TypedDict, total=False):
    '''Provides type-hint for 'ATTRS_TYPES_ARGS' constant'''

    type: Literal[
        'Attr', 'bool', 'callable', 'dict', 'float', 'int', 'list', 'str', 'union'
    ]
    str_pattern: str
    list_len_range: MutableSequence[float]
    list_item_type: 'AttrTypeArgValidation'  # type: ignore
    dict_key_type: 'AttrTypeArgValidation'  # type: ignore
    dict_val_type: 'AttrTypeArgValidation'  # type: ignore
    union_types: MutableSequence['AttrTypeArgValidation']  # type: ignore
    required: Literal[True]


# Reference to all Attr Types and bound Attr Type Args
ATTRS_TYPES_ARGS: MutableMapping[str, MutableMapping[str, AttrTypeArgValidation]] = {
    'ANY': {},
    'ATTR': {
        'types': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {'type': 'str'},
        }
    },
    'ID': {},
    'STR': {'pattern': {'type': 'str'}},
    'INT': {
        'ranges': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {
                'type': 'list',
                'list_len_range': [2, 3],
                'list_item_type': {'type': 'float'},
            },
        }
    },
    'FLOAT': {
        'ranges': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {
                'type': 'list',
                'list_len_range': [2, 3],
                'list_item_type': {'type': 'float'},
            },
        }
    },
    'BOOL': {},
    'LOCALE': {},
    'LOCALES': {},
    'EMAIL': {
        'allowed_domains': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {'type': 'str'},
        },
        'disallowed_domains': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {'type': 'str'},
        },
        'strict_matching': {'type': 'bool'},
    },
    'PHONE': {
        'codes': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {'type': 'str', 'str_pattern': '[0-9]+'},
        }
    },
    'IP': {},
    'URI_WEB': {
        'allowed_domains': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {'type': 'str'},
        },
        'disallowed_domains': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {'type': 'str'},
        },
        'strict_matching': {'type': 'bool'},
    },
    'DATETIME': {
        'ranges': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {
                'type': 'list',
                'list_len_range': [2, 3],
                'list_item_type': {
                    'type': 'str',
                    'str_pattern': r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}(:[0-9]{2}(\.[0-9]{6})?)?|[\-\+][0-9]+[dsmhw]',
                },
            },
        }
    },
    'DATE': {
        'ranges': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {
                'type': 'list',
                'list_len_range': [2, 3],
                'list_item_type': {
                    'type': 'str',
                    'str_pattern': r'[0-9]{4}-[0-9]{2}-[0-9]{2}|[\-\+][0-9]+[dsmhw]',
                },
            },
        }
    },
    'TIME': {
        'ranges': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {
                'type': 'list',
                'list_len_range': [2, 3],
                'list_item_type': {
                    'type': 'str',
                    'str_pattern': r'[0-9]{2}:[0-9]{2}(:[0-9]{2}(\.[0-9]{6})?)?|[\-\+][0-9]+[dsmhw]',
                },
            },
        }
    },
    'FILE': {
        'types': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {'type': 'str'},
        },
        'ratio_ranges': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {
                'type': 'list',
                'list_len_range': [2, 3],
                'list_item_type': {'type': 'float'},
            },
        },
        'dims_ranges': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {
                'type': 'list',
                'list_len_range': [2, 3],
                'list_item_type': {'type': 'float'},
            },
        },
        'size_ranges': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {
                'type': 'list',
                'list_len_range': [2, 3],
                'list_item_type': {'type': 'float'},
            },
        },
    },
    'GEO_POINT': {},
    'LIST': {
        'list': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {'type': 'Attr'},
            'required': True,
        },
        'len_range': {
            'type': 'list',
            'list_len_range': [2, 3],
            'list_item_type': {'type': 'float'},
        },
    },
    'KV_DICT': {
        'key': {
            'type': 'Attr',
            'required': True,
        },
        'val': {
            'type': 'Attr',
            'required': True,
        },
        'len_range': {
            'type': 'list',
            'list_len_range': [2, 3],
            'list_item_type': {'type': 'float'},
        },
        'req': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {'type': 'str'},
        },
    },
    'TYPED_DICT': {
        'dict': {
            'type': 'dict',
            'dict_key_type': {'type': 'str'},
            'dict_val_type': {'type': 'Attr'},
            'required': True,
        }
    },
    'LITERAL': {
        'literal': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {
                'type': 'union',
                'union_types': [
                    {'type': 'str'},
                    {'type': 'int'},
                    {'type': 'float'},
                    {'type': 'bool'},
                ],
            },
            'required': True,
        }
    },
    'UNION': {
        'union': {
            'type': 'list',
            'list_len_range': [1, inf],
            'list_item_type': {'type': 'Attr'},
            'required': True,
        }
    },
    'TYPE': {
        'type': {
            'type': 'union',
            'union_types': [{'type': 'str'}, {'type': 'callable'}],
            'required': True,
        }
    },
}
