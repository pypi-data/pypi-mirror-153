'''Provides 'Var' dataclass'''

from dataclasses import dataclass
from typing import Optional

from nawah.enums import VarType


@dataclass(kw_only=True)
class Var:
    '''Var dataclass serves role of placeholder variable value. It is used to set values in Config
    Attrs dynamically'''

    # pylint: disable=invalid-name

    type: VarType
    var: Optional[str] = None

    @staticmethod
    def ENV(var: str, /) -> 'Var':
        '''Shorthand method to define 'Var' object of type 'ENV' '''
        return Var(type=VarType.ENV, var=var)

    @staticmethod
    def SESSION(var: str, /) -> 'Var':
        '''Shorthand method to define 'Var' object of type 'SESSION' '''
        return Var(type=VarType.SESSION, var=var)

    @staticmethod
    def DOC(var: str, /) -> 'Var':
        '''Shorthand method to define 'Var' object of type 'DOC' '''
        return Var(type=VarType.DOC, var=var)

    @staticmethod
    def L10N(var: str, /) -> 'Var':
        '''Shorthand method to define 'Var' object of type 'L10N' '''
        return Var(type=VarType.L10N, var=var)

    @staticmethod
    def CONFIG(var: str, /) -> 'Var':
        '''Shorthand method to define 'Var' object of type 'CONFIG' '''
        return Var(type=VarType.CONFIG, var=var)

    @staticmethod
    def DATE() -> 'Var':
        '''Shorthand method to define 'Var' object of type 'DATE' '''
        return Var(type=VarType.DATE)

    @staticmethod
    def TIME() -> 'Var':
        '''Shorthand method to define 'Var' object of type 'TIME' '''
        return Var(type=VarType.TIME)

    @staticmethod
    def DATETIME() -> 'Var':
        '''Shorthand method to define 'Var' object of type 'DATETIME' '''
        return Var(type=VarType.DATETIME)

    def __post_init__(self):
        if self.type in [
            VarType.ENV,
            VarType.SESSION,
            VarType.DOC,
            VarType.L10N,
            VarType.CONFIG,
        ]:
            if not self.var:
                raise Exception(
                    f'Var object of type \'{self.type}\' should have value for \'var\' attr'
                )
