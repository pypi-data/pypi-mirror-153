'''Provides exceptions related to validation'''


class MissingAttrException(Exception):
    '''Raised by 'validate_doc' Utility if required 'attr' is missing from 'doc' '''

    status = 400

    def __init__(self, *, attr_name):
        super().__init__(
            MissingAttrException.format_msg(attr_name=attr_name),
            {'attr_name': attr_name},
        )

    @staticmethod
    def format_msg(*, attr_name):
        '''Formats exception message'''

        return f'Missing attr \'{attr_name}\''


class InvalidAttrException(Exception):
    '''Raised by 'validate_attr' Utility if 'attr' has invalid value'''

    status = 400

    def __init__(self, *, attr_name, attr_type, val_type):
        super().__init__(
            InvalidAttrException.format_msg(
                attr_name=attr_name, attr_type=attr_type, val_type=val_type
            ),
            {'attr_name': attr_name, 'attr_type': attr_type, 'val_type': val_type},
        )

    @staticmethod
    def format_msg(*, attr_name, attr_type, val_type):
        '''Formats exception message'''

        return f'Invalid attr \'{attr_name}\' of type \'{val_type}\' with required type \'{attr_type}\''
