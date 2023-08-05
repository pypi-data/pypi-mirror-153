'''Provides 'Query' and related classes and types'''

import copy
from typing import (TYPE_CHECKING, Any, Literal, MutableMapping,
                    MutableSequence, Optional, TypedDict, Union, cast)

from nawah.exceptions import InvalidQueryArgException, UnknownQueryArgException

if TYPE_CHECKING:
    from nawah.types import NawahQuery, NawahQuerySpecial


SPECIAL_ATTRS = [
    '$search',
    '$sort',
    '$skip',
    '$limit',
    '$extn',
    '$soft',
    '$attrs',
    '$group',
    '$geo_near',
]


class QueryIndexRecord(TypedDict):
    '''Provides type-hint for a single record in Query Index'''

    oper: str
    path: str
    val: Any


class Query(list):
    '''Compiles a list-based Nawah Query into an object that is indexable per \'Query Args\', \'Query Args Opers\'.
    Class provides secure methods to access and manipulate values in Query'''

    _query: 'NawahQuery'
    _special: 'NawahQuerySpecial'
    _index: MutableMapping[str, MutableSequence[QueryIndexRecord]]

    def __init__(self, query: Union['NawahQuery', 'Query']):
        self._query = query
        if isinstance(self._query, Query):
            query = cast(Query, query)
            self._query = query._query + [query._special]
        self._special = {}
        self._index = {}
        self._create_index(self._query)
        super().__init__(self._query)

    def __repr__(self):
        return str(self._query + [self._special])

    def _create_index(self, query: 'NawahQuery', path=None):
        if not path:
            path = []
            self._index = {}
        for i, _ in enumerate(query):
            if isinstance(query[i], dict):
                del_attrs = []
                for attr in query[i].keys():
                    if attr in SPECIAL_ATTRS:
                        self._special[attr] = query[i][attr]  # type: ignore
                        del_attrs.append(attr)
                    elif attr.startswith('__or'):
                        self._create_index(query[i][attr], path=path + [i, attr])  # type: ignore
                    else:
                        if (
                            isinstance(query[i][attr], dict)  # type: ignore
                            and len(query[i][attr].keys()) == 1  # type: ignore
                            and list(query[i][attr].keys())[0][0] == '$'  # type: ignore
                        ):
                            attr_oper = list(query[i][attr].keys())[0]  # type: ignore
                        else:
                            attr_oper = '$eq'
                        if attr not in self._index:
                            self._index[attr] = []
                        if isinstance(query[i][attr], dict) and '_id' in query[i][attr]:  # type: ignore
                            query[i][attr] = query[i][attr]['_id']  # type: ignore
                        validate_query_arg(arg_name=attr, arg_oper=attr_oper, arg_val=query[i][attr])  # type: ignore
                        self._index[attr].append(
                            {
                                'oper': attr_oper,
                                'path': path + [i],
                                'val': query[i][attr],  # type: ignore
                            }
                        )
                for attr in del_attrs:
                    del query[i][attr]  # type: ignore
            elif isinstance(query[i], list):
                self._create_index(query[i], path=path + [i])  # type: ignore
            else:
                raise ValueError(
                    f'Type of Query Arg is of type \'{type(query[i])}\'. Only types \'dict, list\' are allowed.'
                )
        if not path:
            self._query = self._sanitise_query()

    def _sanitise_query(self, query: 'NawahQuery' = None):
        if query is None:
            query = self._query
        query = cast('NawahQuery', query)
        query_shadow = []
        for step in query:
            if isinstance(step, dict):
                for attr in step.keys():
                    if attr.startswith('__or'):
                        step[attr] = self._sanitise_query(step[attr])  # type: ignore
                        if len(step[attr]):  # type: ignore
                            query_shadow.append(step)
                            break
                    elif attr[0] != '$':
                        query_shadow.append(step)
                        break
            elif isinstance(step, list):
                step = self._sanitise_query(step)
                if len(step) != 0:
                    query_shadow.append(step)
        return query_shadow

    def __deepcopy__(self, memo):
        return Query(copy.deepcopy(self._query + [self._special]))

    def append(self, obj: Any):
        self._query.append(obj)
        self._create_index(self._query)
        super().__init__(self._query)

    def __contains__(self, attr):
        if attr in SPECIAL_ATTRS:
            return attr in self._special

        if ':' in attr:
            attr_index, attr_oper = attr.split(':')
        else:
            attr_index = attr
            attr += ':$eq'
            attr_oper = '$eq'

        if attr_index in self._index:
            for val in self._index[attr_index]:
                if attr_oper in (val['oper'], '*'):
                    return True

        return False

    def __getitem__(self, attr):
        if attr in SPECIAL_ATTRS:
            return self._special[attr]

        attrs = []
        vals = []
        paths: MutableSequence[MutableSequence[int]] = []
        indexes = []
        attr_filter: Optional[str] = None
        oper_filter: Optional[str] = None

        if attr.split(':')[0] != '*':
            attr_filter = attr.split(':')[0]

        if ':' not in attr:
            oper_filter = '$eq'
            attr += ':$eq'
        elif ':*' not in attr:
            oper_filter = attr.split(':')[1]

        for index_attr in self._index:
            if attr_filter and index_attr != attr_filter:
                continue
            i = 0
            for val in self._index[index_attr]:
                if not oper_filter or (oper_filter and val['oper'] == oper_filter):
                    attrs.append(index_attr)
                    # [TODO] Simplify this condition by enforcing Query Args with $eq Query Oper are always stripped down to value
                    if not oper_filter or (
                        oper_filter == '$eq'
                        and (
                            not isinstance(val['val'], dict) or '$eq' not in val['val']
                        )
                    ):
                        vals.append(val['val'])
                    else:
                        vals.append(val['val'][oper_filter])
                    paths.append(val['path'])
                    indexes.append(i)
                    i += 1
        return QueryAttrList(
            query=self, attrs=attrs, paths=paths, indexes=indexes, vals=vals
        )

    def __setitem__(self, attr, val):
        if attr[0] != '$':
            raise Exception('Non-special attrs can only be updated by attr index.')
        self._special[attr] = val

    def __delitem__(self, attr):
        if attr[0] != '$':
            raise Exception('Non-special attrs can only be deleted by attr index.')
        del self._special[attr]


class QueryAttrList(list):
    '''A meta class that creates references to specific \'Query Arg\' in a \'Query\'
    object, to allow manipulation or deletion of specific \'Query Arg\' value'''

    def __init__(
        self,
        *,
        query: Query,
        attrs: MutableSequence[str],
        paths: MutableSequence[MutableSequence[int]],
        indexes: MutableSequence[int],
        vals: MutableSequence[Any],
    ):
        self._query = query
        self._attrs = attrs
        self._paths = paths
        self._indexes = indexes
        self._vals = vals
        super().__init__(vals)

    def __setitem__(self, item, val):
        if item == '*':
            for i in range(len(self._vals)):
                self.__setitem__(i, val)
        else:
            instance_attr = self._query._query
            for path_part in self._paths[item]:
                instance_attr = instance_attr[path_part]
            instance_attr[self._attrs[item].split(':')[0]] = val
            self._query._create_index(self._query._query)

    def __delitem__(self, item):
        if item == '*':
            for i in range(len(self._vals)):
                self.__delitem__(i)
        else:
            instance_attr = self._query._query
            for path_part in self._paths[item]:
                instance_attr = instance_attr[path_part]
            del instance_attr[self._attrs[item].split(':')[0]]
            self._query._create_index(self._query._query)

    def replace_attr(self, item: Union[Literal['*'], int], new_attr: str):
        '''Replaces attr name of \'Query Arg\', retaining the value[s] and position in \'Query\' object'''

        if item == '*':
            for i in range(len(self._vals)):
                self.replace_attr(i, new_attr)
            return

        instance_attr = self._query._query
        for path_part in self._paths[item]:
            instance_attr = instance_attr[path_part]  # type: ignore
        # Set new attr
        instance_attr[new_attr] = instance_attr[self._attrs[item].split(':')[0]]  # type: ignore
        # Delete old attr
        del instance_attr[self._attrs[item].split(':')[0]]  # type: ignore
        # Update index
        self._query._create_index(self._query._query)


def validate_query_arg(*, arg_name, arg_oper, arg_val):
    '''Validates value of provided \'Query Arg\' per \'Query Arg Oper\'. If failed, raises
    \'InvalidQueryArgException\' or \'UnknownQueryArgException\' if \'Query Arg Oper\' is unknow'''

    if arg_oper in ['$ne', '$eq']:
        return

    if arg_oper in ['$gt', '$gte', '$lt', '$lte']:
        if type(arg_val[arg_oper]) not in [str, int, float]:
            raise InvalidQueryArgException(
                arg_name=arg_name,
                arg_oper=arg_oper,
                arg_type=[str, int, float],
                arg_val=arg_val[arg_oper],
            )
    elif arg_oper in ['$all', '$in', '$nin']:
        if not isinstance(arg_val[arg_oper], list):
            # [TODO] Validate why this was added
            # or not len(arg_val[arg_oper]):
            raise InvalidQueryArgException(
                arg_name=arg_name,
                arg_oper=arg_oper,
                arg_type=list,
                arg_val=arg_val[arg_oper],
            )
    elif arg_oper == '$regex':
        if isinstance(arg_val[arg_oper], str):
            raise InvalidQueryArgException(
                arg_name=arg_name,
                arg_oper=arg_oper,
                arg_type=str,
                arg_val=arg_val[arg_oper],
            )
    else:
        raise UnknownQueryArgException(arg_name=arg_name, arg_oper=arg_oper)
