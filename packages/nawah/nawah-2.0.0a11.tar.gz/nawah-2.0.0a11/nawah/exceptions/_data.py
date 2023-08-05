'''Provides exceptions related to Data'''


class UnknownDeleteStrategyException(Exception):
    '''Raised by 'Data.delete' if passed unknown 'DeleteStrategy' '''
