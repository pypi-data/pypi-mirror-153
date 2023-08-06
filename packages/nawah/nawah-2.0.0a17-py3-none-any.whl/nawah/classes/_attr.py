'''Provides 'Attr' dataclass'''

import datetime
from dataclasses import dataclass
from typing import (TYPE_CHECKING, Any, Callable, Mapping, MutableMapping,
                    Optional, Sequence, Union)

from nawah.enums import AttrType

if TYPE_CHECKING:
    from ._default import Default
    from ._extn import Extn


@dataclass(kw_only=True)
class Attr:
    '''Attr dataclass serves role of defining an Attr Type Set, which
    instructs Nawah of allowed data type for a specific value'''

    # pylint: disable=invalid-name, redefined-builtin, too-many-public-methods

    desc: Optional[str]
    type: AttrType
    args: MutableMapping[str, Any]

    def __post_init__(self):
        self._default = None
        self._extn = None
        self._valid = False

    @property
    def default(self) -> Optional['Default']:
        '''Exposes _default attribute'''
        return self._default

    @default.setter
    def default(self, default):
        self._default = default

    @property
    def extn(self) -> Optional['Extn']:
        '''Exposes _extn attribute'''
        return self._extn

    @extn.setter
    def extn(self, extn):
        self._extn = extn

    @property
    def valid(self) -> bool:
        '''Exposes _valid attribute'''
        return self._valid

    @valid.setter
    def valid(self, valid):
        self._valid = valid

    @staticmethod
    def ANY(desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'ANY' '''
        return Attr(desc=desc, type=AttrType.ANY, args={})

    @staticmethod
    def ATTR(desc: str = None, type: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'ATTR' '''
        return Attr(desc=desc, type=AttrType.ATTR, args={'type': type})

    @staticmethod
    def ID(desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'ID' '''
        return Attr(desc=desc, type=AttrType.ID, args={})

    @staticmethod
    def STR(pattern: str = None, desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'STR' '''
        return Attr(desc=desc, type=AttrType.STR, args={'pattern': pattern})

    @staticmethod
    def INT(ranges: Sequence[Sequence[float]] = None, desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'INT' '''
        return Attr(desc=desc, type=AttrType.INT, args={'ranges': ranges})

    @staticmethod
    def FLOAT(ranges: Sequence[Sequence[float]] = None, desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'FLOAT' '''
        return Attr(desc=desc, type=AttrType.FLOAT, args={'ranges': ranges})

    @staticmethod
    def BOOL(desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'BOOL' '''
        return Attr(desc=desc, type=AttrType.BOOL, args={})

    @staticmethod
    def LOCALE(desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'LOCALE' '''
        return Attr(desc=desc, type=AttrType.LOCALE, args={})

    @staticmethod
    def LOCALES(desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'LOCALES' '''
        return Attr(desc=desc, type=AttrType.LOCALES, args={})

    @staticmethod
    def EMAIL(
        allowed_domains: Sequence[str] = None,
        disallowed_domains: Sequence[str] = None,
        strict_matching: bool = None,
        desc: str = None,
    ) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'EMAIL' '''
        return Attr(
            desc=desc,
            type=AttrType.EMAIL,
            args={
                'allowed_domains': allowed_domains,
                'disallowed_domains': disallowed_domains,
                'strict_matching': strict_matching,
            },
        )

    @staticmethod
    def PHONE(codes: Sequence[str] = None, desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'PHONE' '''
        return Attr(desc=desc, type=AttrType.PHONE, args={'codes': codes})

    @staticmethod
    def IP(desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'IP' '''
        return Attr(desc=desc, type=AttrType.IP, args={})

    @staticmethod
    def URI_WEB(
        allowed_domains: Sequence[str] = None,
        disallowed_domains: Sequence[str] = None,
        strict_matching: bool = None,
        desc: str = None,
    ) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'URI_WEB' '''
        return Attr(
            desc=desc,
            type=AttrType.URI_WEB,
            args={
                'allowed_domains': allowed_domains,
                'disallowed_domains': disallowed_domains,
                'strict_matching': strict_matching,
            },
        )

    @staticmethod
    def DATETIME(
        ranges: Sequence[Sequence[datetime.datetime]] = None,
        desc: str = None,
    ) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'DATETIME' '''
        return Attr(desc=desc, type=AttrType.DATETIME, args={'ranges': ranges})

    @staticmethod
    def DATE(
        ranges: Sequence[Sequence[datetime.date]] = None, desc: str = None
    ) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'DATE' '''
        return Attr(desc=desc, type=AttrType.DATE, args={'ranges': ranges})

    @staticmethod
    def TIME(ranges: Sequence[Sequence[str]] = None, desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'TIME' '''
        return Attr(desc=desc, type=AttrType.TIME, args={'ranges': ranges})

    @staticmethod
    def FILE(
        types: Sequence[str] = None,
        ratio_ranges: Sequence[Sequence[float]] = None,
        dims_ranges: Sequence[Sequence[float]] = None,
        size_ranges: Sequence[Sequence[float]] = None,
        desc: str = None,
    ) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'FILE' '''
        return Attr(
            desc=desc,
            type=AttrType.FILE,
            args={
                'types': types,
                'ratio_ranges': ratio_ranges,
                'dims_ranges': dims_ranges,
                'size_ranges': size_ranges,
            },
        )

    @staticmethod
    def GEO_POINT(desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'GEO_POINT' '''
        return Attr(desc=desc, type=AttrType.GEO_POINT, args={})

    @staticmethod
    def LIST(
        list: Sequence['Attr'],
        len_range: Sequence[float] = None,
        desc: str = None,
    ) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'LIST' '''
        return Attr(
            desc=desc, type=AttrType.LIST, args={'list': list, 'len_range': len_range}
        )

    @staticmethod
    def KV_DICT(
        key: 'Attr',
        val: 'Attr',
        req: Sequence[str] = None,
        len_range: Sequence[float] = None,
        desc: str = None,
    ) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'KV_DICT' '''
        return Attr(
            desc=desc,
            type=AttrType.KV_DICT,
            args={'key': key, 'val': val, 'req': req, 'len_range': len_range},
        )

    @staticmethod
    def TYPED_DICT(dict: Mapping[str, 'Attr'], desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'TYPED_DICT' '''
        return Attr(desc=desc, type=AttrType.TYPED_DICT, args={'dict': dict})

    @staticmethod
    def LITERAL(
        literal: Sequence[Union[str, int, float, bool]], desc: str = None
    ) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'LITERAL' '''
        return Attr(desc=desc, type=AttrType.LITERAL, args={'literal': literal})

    @staticmethod
    def UNION(union: Sequence['Attr'], desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'UNION' '''
        return Attr(desc=desc, type=AttrType.UNION, args={'union': union})

    @staticmethod
    def TYPE(type: Union[Callable, str], desc: str = None) -> 'Attr':
        '''Shorthand method to define 'Attr' object of type 'TYPE' '''
        return Attr(desc=desc, type=AttrType.TYPE, args={'type': type})
