'''Provides Exception classes for Base Functions'''

# START: Shared exceptions
class UtilityModuleDataCallException(Exception):
    '''Raised if a data call was made for a Utility Module'''

    status = 400

    def __init__(self, *, module_name, func_name):
        super().__init__(
            UtilityModuleDataCallException.format_msg(
                module_name=module_name, func_name=func_name
            ),
            {'module_name': module_name, 'func_name': func_name},
        )

    @staticmethod
    def format_msg(*, module_name, func_name):
        '''Formats exception message'''

        return (
            f'Nawah Function \'{func_name}\' can\'t be called on Nawah Utility module '
            f'\'{module_name}\''
        )


class DuplicateUniqueException(Exception):
    '''Raised if 'create', 'update' call has at least one 'unique_attr' value in 'doc'
    that matches another doc'''

    status = 400

    def __init__(self, *, unique_attrs):
        super().__init__(
            DuplicateUniqueException.format_msg(unique_attrs=unique_attrs),
            {'unique_attrs': unique_attrs},
        )

    @staticmethod
    def format_msg(*, unique_attrs):
        '''Formats exception message'''

        return f'A doc matching at least one of \'{unique_attrs}\' already exists'


class InvalidDocException(Exception):
    '''Raised if 'delete_file', 'retrieve_file' call 'query' does not return any doc'''

    status = 400

    def __init__(self, *, doc_id):
        super().__init__(
            InvalidDocException.format_msg(doc_id=doc_id), {'doc_id': doc_id}
        )

    @staticmethod
    def format_msg(*, doc_id):
        '''Formats exception message'''

        return f'Query for doc with \'_id\' \'{doc_id}\' returned no results'


# END: Shared exceptions

# START: create exceptions
class NoDocCreatedException(Exception):
    '''Raised if 'create' call creates no doc'''

    status = 400

    def __init__(self, *, module_name):
        super().__init__(
            NoDocCreatedException.format_msg(module_name=module_name),
            {'module_name': module_name},
        )

    @staticmethod
    def format_msg(*, module_name):
        '''Formats exception message'''

        return f'No documents were created for module \'{module_name}\''


# END: create exceptions

# START: delete exceptions
class NoDocDeletedException(Exception):
    '''Raised if 'delete' call deletes no doc'''

    status = 400

    def __init__(self, *, module_name):
        super().__init__(
            NoDocDeletedException.format_msg(module_name=module_name),
            {'module_name': module_name},
        )

    @staticmethod
    def format_msg(*, module_name):
        '''Formats exception message'''

        return f'No documents were deleted for module \'{module_name}\''


# END: delete exceptions

# START: read exceptions
class NoDocFoundException(Exception):
    '''Raised if 'read' call founds no doc'''

    status = 400

    def __init__(self, *, module_name):
        super().__init__(
            NoDocFoundException.format_msg(module_name=module_name),
            {'module_name': module_name},
        )

    @staticmethod
    def format_msg(*, module_name):
        '''Formats exception message'''

        return f'No documents were found for module \'{module_name}\''


# END: read exceptions

# START: delete_file exceptions
class InvalidDeleteFileDocAttrException(Exception):
    '''Raised if 'delete_file' call 'query' returns doc with attr not valid for operation'''

    status = 400

    def __init__(self, *, doc_id, attr_name):
        super().__init__(
            InvalidDeleteFileDocAttrException.format_msg(
                doc_id=doc_id, attr_name=attr_name
            ),
            {'doc_id': doc_id, 'attr_name': attr_name},
        )

    @staticmethod
    def format_msg(*, doc_id, attr_name):
        '''Formats exception message'''

        return f'Query for doc with \'_id\' \'{doc_id}\' returned doc with invalid value for attr \'{attr_name}\''


class InvalidDeleteFileIndexException(Exception):
    '''Raised if 'delete_file' call 'query' returns doc with index for call not valid for operation'''

    status = 400

    def __init__(self, *, doc_id, attr_name, index):
        super().__init__(
            InvalidDeleteFileIndexException.format_msg(
                doc_id=doc_id, attr_name=attr_name, index=index
            ),
            {'doc_id': doc_id, 'attr_name': attr_name, 'index': index},
        )

    @staticmethod
    def format_msg(*, doc_id, attr_name, index):
        '''Formats exception message'''

        return f'Index \'{index}\' for attr \'{attr_name}\' for doc with \'_id\' \'{doc_id}\' is invalid'


class InvalidDeleteFileIndexValueException(Exception):
    '''Raised if 'delete_file' call 'query' returns doc with index value for call not valid for operation'''

    status = 400

    def __init__(self, *, doc_id, attr_name, index, index_val_type):
        super().__init__(
            InvalidDeleteFileIndexValueException.format_msg(
                doc_id=doc_id,
                attr_name=attr_name,
                index=index,
                index_val_type=index_val_type,
            ),
            {
                'doc_id': doc_id,
                'attr_name': attr_name,
                'index': index,
                'index_val_type': index_val_type,
            },
        )

    @staticmethod
    def format_msg(*, doc_id, attr_name, index, index_val_type):
        '''Formats exception message'''

        return f'Index \'{index}\' for attr \'{attr_name}\' for doc with \'_id\' \'{doc_id}\' is of invalid type \'{index_val_type}\''


class InvalidDeleteFileMismatchNameException(Exception):
    '''Raised if 'delete_file' call 'query' returns doc with index value file name not matching 'query' '''

    status = 400

    def __init__(self, *, doc_id, attr_name, index, query_file_name, index_file_name):
        super().__init__(
            InvalidDeleteFileMismatchNameException.format_msg(
                doc_id=doc_id,
                attr_name=attr_name,
                index=index,
                query_file_name=query_file_name,
                index_file_name=index_file_name,
            ),
            {
                'doc_id': doc_id,
                'attr_name': attr_name,
                'index': index,
                'query_file_name': query_file_name,
                'index_file_name': index_file_name,
            },
        )

    @staticmethod
    def format_msg(*, doc_id, attr_name, index, query_file_name, index_file_name):
        '''Formats exception message'''

        return f'Index \'{index}\' for attr \'{attr_name}\' for doc with \'_id\' \'{doc_id}\' is for file \'{index_file_name}\', not \'{query_file_name}\''


# END: delete_file exceptions

# START: obtain_lock exceptions
class FailedObtainLockException(Exception):
    '''Raised if 'obtain_lock' call failed to obtain lock'''

    status = 400

    def __init__(self, *, module_name):
        super().__init__(
            FailedObtainLockException.format_msg(module_name=module_name),
            {'module_name': module_name},
        )

    @staticmethod
    def format_msg(*, module_name):
        '''Formats exception message'''

        return f'Failed to obtain lock for \'{module_name}\''


# END: obtain_lock exceptions

# START: delete_lock exceptions
class FailedDeleteLockException(Exception):
    '''Raised if 'obtain_lock','delete_lock' call failed to deleted obtaiend lock'''

    status = 500

    def __init__(self, *, module_name, lock_id):
        super().__init__(
            FailedDeleteLockException.format_msg(
                module_name=module_name, lock_id=lock_id
            ),
            {'module_name': module_name, 'lock_id': lock_id},
        )

    @staticmethod
    def format_msg(*, module_name, lock_id):
        '''Formats exception message'''

        return f'Failed to delete lock \'{lock_id}\' for \'{module_name}\'. Delete manually now'


# END: delete_lock exceptions

# START: update exceptions
class UpdateMultiUniqueException(Exception):
    '''Raised if 'update' call is attempted on multiple docs
    where at least one 'unique_attr' is present in 'update_doc' '''

    status = 400

    def __init__(self):
        super().__init__(UpdateMultiUniqueException.format_msg())

    @staticmethod
    def format_msg():
        '''Formats exception message'''

        return (
            'Update call query has more than one doc as results. This would result in'
            'duplication'
        )


class EmptyUpdateDocException(Exception):
    '''Raised if 'update' call has empty \'doc\' '''

    status = 400

    def __init__(self, *, module_name):
        super().__init__(
            EmptyUpdateDocException.format_msg(module_name=module_name),
            {'module_name': module_name},
        )

    @staticmethod
    def format_msg(*, module_name):
        '''Formats exception message'''

        return f'Update \'doc\' is empty for module \'{module_name}\''


class NoDocUpdatedException(Exception):
    '''Raised if 'update' call updates no doc'''

    status = 400

    def __init__(self, *, module_name):
        super().__init__(
            NoDocUpdatedException.format_msg(module_name=module_name),
            {'module_name': module_name},
        )

    @staticmethod
    def format_msg(*, module_name):
        '''Formats exception message'''

        return f'No documents were updated for module \'{module_name}\''


# END: update exceptions

# START: retrieve_file exceptions
class FileNotFoundException(Exception):
    '''Raised by 'retrieve_file' if failed to locate attr, or attr does not match requested file name'''

    status = 400

    def __init__(self, *, doc_id, attr_name, file_name):
        super().__init__(
            FileNotFoundException.format_msg(
                doc_id=doc_id, attr_name=attr_name, file_name=file_name
            ),
            {'doc_id': doc_id, 'attr_name': attr_name, 'file_name': file_name},
        )

    @staticmethod
    def format_msg(*, doc_id, attr_name, file_name):
        '''Formats exception message'''

        return f'Failed to find file for doc \'_id\' \'{doc_id}\', attr \'{attr_name}\', file \'{file_name}\''


class FileNotImageException(Exception):
    '''Raised by 'retrieve_file' if attemtped to generate thumbnail of non-image file'''

    status = 400

    def __init__(self, *, doc_id, attr_name, file_name, file_type):
        super().__init__(
            FileNotImageException.format_msg(
                doc_id=doc_id,
                attr_name=attr_name,
                file_name=file_name,
                file_type=file_type,
            ),
            {
                'doc_id': doc_id,
                'attr_name': attr_name,
                'file_name': file_name,
                'file_type': file_type,
            },
        )

    @staticmethod
    def format_msg(*, doc_id, attr_name, file_name, file_type):
        '''Formats exception message'''

        return f'Can\'t generate thumbnail for file for doc \'_id\' \'{doc_id}\', attr \'{attr_name}\', file \'{file_name}\', of type \'{file_type}\''


# END: retrieve_file exceptions
