'''Provides 'SysDoc' dataclass'''

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional, cast

from bson import ObjectId

if TYPE_CHECKING:
    from nawah.types import NawahDoc

# [TODO] Create custom exceptions


@dataclass(kw_only=True)
class SysDoc:
    '''SysDoc dataclass serves role of defining items of 'docs' Config Attr which
    are docs created when an app is laucnhed, or as results of Nawah operations'''

    module: str
    key: Optional[str] = None
    skip_args: bool = False
    doc: Optional['NawahDoc'] = None

    @property
    def key_value(self) -> Any:
        '''Returns value for key 'key' from 'doc'. Raises ..., if 'doc' is not set'''

        if not self.doc:
            raise Exception('SysDoc instance was initialised with no \'doc\'.')
        self.key = cast(str, self.key)
        return self.doc[self.key]

    def __post_init__(self):
        if self.doc is not None:
            if not isinstance(self.doc, dict):
                raise Exception(
                    f'Argument \'doc\' is not a valid \'NawahDoc\'. Expecting type \'dict\' but got \'{type(self.doc)}\'.'
                )
            self.doc = cast('NawahDoc', self.doc)
            if not self.key:
                self.key = '_id'
            if self.key not in self.doc.keys():
                raise Exception(f'Attr \'{self.key}\' is not present on \'doc\'.')
            if self.key == '_id' and not isinstance(self.doc['_id'], ObjectId):
                raise Exception(
                    f'Invalid attr \'_id\' of type \'{type(self.doc["_id"])}\' with required type \'ID\''
                )
        else:
            if self.key or self.skip_args:
                raise Exception(
                    'Arguments \'attr, skip_args\' should only be used with \'doc\'.'
                )
