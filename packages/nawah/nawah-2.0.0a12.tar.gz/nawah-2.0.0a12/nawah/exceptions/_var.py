'''Provides exceptions related to 'var_value' Utility'''


class InvalidLocaleException(Exception):
    '''Raied by 'var_value' Utility if 'locale' is not defined in runtime config'''

    def __init__(self, *, locale):
        super().__init__(
            InvalidLocaleException.format_msg(locale=locale),
            {'locale': locale},
        )

    @staticmethod
    def format_msg(*, locale):
        '''Formats exception message'''
        return f'Invalid locale \'{locale}\''


class InvalidVarException(Exception):
    '''Raied by 'var_value' Utility if failed to extract value of 'var' '''

    def __init__(self, *, var):
        super().__init__(
            InvalidVarException.format_msg(var=var),
            {'var': var},
        )

    @staticmethod
    def format_msg(*, var):
        '''Formats exception message'''
        return f'Invalid var \'{var}\''
