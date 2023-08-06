'''Provides exceptions related to Query'''

from typing import Any, Literal


class InvalidQueryArgException(Exception):
    '''Raised by \'Query.validate_arg\' if an invalid \'Query Arg\' is detected'''

    status = 400

    def __init__(
        self,
        *,
        arg_name: str,
        arg_oper: Literal[
            '$ne',
            '$eq',
            '$gt',
            '$gte',
            '$lt',
            '$lte',
            '$all',
            '$in',
            '$nin',
            '$regex',
        ],
        arg_type: Any,
        arg_val: Any,
    ):
        super().__init__(
            InvalidQueryArgException.format_msg(
                arg_name=arg_name, arg_oper=arg_oper, arg_type=arg_type, arg_val=arg_val
            ),
            {
                'arg_name': arg_name,
                'arg_oper': arg_oper,
                'arg_type': arg_type,
                'arg_val': arg_val,
            },
        )

    @staticmethod
    def format_msg(*, arg_name, arg_oper, arg_type, arg_val):
        '''Formats exception message'''

        return f'Invalid value for Query Arg \'{arg_name}\' with Query Arg Oper \'{arg_oper}\' expecting type \'{arg_type}\' but got \'{arg_val}\''


class UnknownQueryArgException(Exception):
    '''Raised by \'Query.validate_arg\' if an unknown \'Query Arg\' is detected'''

    status = 400

    def __init__(
        self,
        *,
        arg_name: str,
        arg_oper: Literal[
            '$ne',
            '$eq',
            '$gt',
            '$gte',
            '$lt',
            '$lte',
            '$all',
            '$in',
            '$nin',
            '$regex',
        ],
    ):
        super().__init__(
            UnknownQueryArgException.format_msg(arg_name=arg_name, arg_oper=arg_oper),
            {'arg_name': arg_name, 'arg_oper': arg_oper},
        )

    @staticmethod
    def format_msg(*, arg_name, arg_oper):
        '''Formats exception message'''

        return f'Unknown Query Arg Oper \'{arg_oper}\' for Query Arg \'{arg_name}\''
