'''Provides exceptions related to Nawah Function'''

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types import ResultsArgs


class FuncException(Exception):
    '''Raised by \'call\' Utility when encounters an exception raised
    by Nawah Function callable'''

    def __init__(self, *, status: int, msg: str, args: 'ResultsArgs'):
        if 'code' not in args:
            raise Exception(
                'Invalid value for \'args\' for FuncException. Missing item \'code\''
            )

        super().__init__(msg, {'status': status, 'args': args})


class MissingQueryAttrException(Exception):
    '''Raied by '_check_query_attrs' if 'attr_name' is missing from checked Query object'''

    status = 400

    def __init__(self, *, attr_name):
        super().__init__(
            MissingQueryAttrException.format_msg(attr_name=attr_name),
            {'attr_name': attr_name},
        )

    @staticmethod
    def format_msg(*, attr_name):
        '''Formats exception message'''

        return f'Missing attr \'{attr_name}\' from Query'


class InvalidQueryAttrException(Exception):
    '''Raised by '_check_query_attrs' if 'attr' has invalid value'''

    status = 400

    def __init__(self, *, attr_name, attr_type, val_type):
        super().__init__(
            InvalidQueryAttrException.format_msg(
                attr_name=attr_name, attr_type=attr_type, val_type=val_type
            ),
            {'attr_name': attr_name, 'attr_type': attr_type, 'val_type': val_type},
        )

    @staticmethod
    def format_msg(*, attr_name, attr_type, val_type):
        '''Formats exception message'''

        return (
            f'Invalid attr \'{attr_name}\' of type \'{val_type}\' with required type '
            f'\'{attr_type}\''
        )


class InvalidQueryException(Exception):
    '''Raised by '_check_query_attrs', when fail to match all 'query_attrs' sets'''

    status = 400

    def __init__(self, *, query_attrs_sets):
        super().__init__(
            InvalidQueryException.format_msg(query_attrs_sets=query_attrs_sets),
            {'query_attrs_sets': query_attrs_sets},
        )

    @staticmethod
    def format_msg(*, query_attrs_sets):
        '''Formats exception message'''

        return f'Invalid Query. Matched against: {query_attrs_sets}'


class MissingDocAttrException(Exception):
    '''Raied by '_check_doc_attrs' if 'attr_name' is missing from checked Doc object'''

    status = 400

    def __init__(self, *, attr_name):
        super().__init__(
            MissingDocAttrException.format_msg(attr_name=attr_name),
            {'attr_name': attr_name},
        )

    @staticmethod
    def format_msg(*, attr_name):
        '''Formats exception message'''

        return f'Missing attr \'{attr_name}\' from Doc'


class InvalidDocAttrException(Exception):
    '''Raised by '_check_doc_attrs' if 'attr' has invalid value'''

    status = 400

    def __init__(self, *, attr_name, attr_type, val_type):
        super().__init__(
            InvalidDocAttrException.format_msg(
                attr_name=attr_name, attr_type=attr_type, val_type=val_type
            ),
            {'attr_name': attr_name, 'attr_type': attr_type, 'val_type': val_type},
        )

    @staticmethod
    def format_msg(*, attr_name, attr_type, val_type):
        '''Formats exception message'''

        return (
            f'Invalid attr \'{attr_name}\' of type \'{val_type}\' with required type '
            f'\'{attr_type}\''
        )


class InvalidDocException(Exception):
    '''Raised by '_check_doc_attrs', when fail to match all 'doc_attrs' sets'''

    status = 400

    def __init__(self, *, doc_attrs_sets):
        super().__init__(
            InvalidDocException.format_msg(doc_attrs_sets=doc_attrs_sets),
            {'doc_attrs_sets': doc_attrs_sets},
        )

    @staticmethod
    def format_msg(*, doc_attrs_sets):
        '''Formats exception message'''

        return f'Invalid Doc. Matched against: {doc_attrs_sets}'
