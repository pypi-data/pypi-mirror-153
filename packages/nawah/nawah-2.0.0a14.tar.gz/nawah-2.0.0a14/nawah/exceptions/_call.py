'''Provides exceptions related to 'call' Utility'''


class InvalidCallEndpointException(Exception):
    '''Raised by 'call' Utility if value for arg 'endpoint' is invalid'''

    status = 400

    def __init__(self, *, endpoint):
        super().__init__(
            InvalidCallEndpointException.format_msg(endpoint=endpoint),
            {'endpoint': endpoint},
        )

    @staticmethod
    def format_msg(*, endpoint):
        '''Formats exception message'''

        return f'Invliad endpoint format: \'{endpoint}\''


class InvalidModuleException(Exception):
    '''Raised by 'call' Utility if endpoint points to non-existent Nawah Module'''

    status = 404

    def __init__(self, *, module_name):
        super().__init__(
            InvalidModuleException.format_msg(module_name=module_name),
            {'module_name': module_name},
        )

    @staticmethod
    def format_msg(*, module_name):
        '''Formats exception message'''

        return f'Nawah Module \'{module_name}\' is not defined'


class InvalidFuncException(Exception):
    '''Raised by 'call' Utility if endpoint points to non-existent Nawah Function'''

    status = 404

    def __init__(self, *, module_name, func_name):
        super().__init__(
            InvalidFuncException.format_msg(
                module_name=module_name, func_name=func_name
            ),
            {'module_name': module_name, 'func_name': func_name},
        )

    @staticmethod
    def format_msg(*, module_name, func_name):
        '''Formats exception message'''

        return f'Nawah Module \'{module_name}\' does not have Function \'{func_name}\' defined'


class NotPermittedException(Exception):
    '''Raised by 'check_permissions' Utility if failed to match Permissions Sets for current
    session user'''

    status = 403

    def __init__(self, *, module_name, func_name):
        super().__init__(
            NotPermittedException.format_msg(
                module_name=module_name, func_name=func_name
            ),
            {'module_name': module_name, 'func_name': func_name},
        )

    @staticmethod
    def format_msg(*, module_name, func_name):
        '''Formats exception message'''

        return f'Not permitted to access \'{module_name}\'.\'{func_name}\''
