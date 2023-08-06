'''Provides collection of validation tools used by Nawah and
can be used by Nawah Apps to use with complex business-logic'''

from ._attr import validate_attr, validate_doc
from ._type import validate_type

__all__ = ['validate_attr', 'validate_doc', 'validate_type']
