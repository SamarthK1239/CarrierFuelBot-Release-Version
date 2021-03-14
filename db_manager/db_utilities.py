from typing import Any, Dict, Tuple, Union
from sqlalchemy import Table
from sqlalchemy.sql.dml import Delete, Update
from sqlalchemy.sql.selectable import Select


def build_query(table: Table, method: str, filters: Dict[str, Dict[str, Any]] = None) -> Tuple[Union[Select, Update], Dict[str, Any]]:
    query: Union[Select, Update, Delete] = None
    method = method.lower()

    if method == 'select':
        query = table.select()
    elif method == 'update':
        query = table.update()
    elif method == 'delete':
        query = table.delete()
    values = {}

    if filters:
        if filters.get('equalTo') != None:
            for filter_name in filters['equalTo'].keys():
                if filters['equalTo'].get(filter_name) != None:
                    query = query.where(getattr(table.c, filter_name) == '')
                    values[filter_name + '_1'] = filters['equalTo'].get(filter_name)

        if filters.get('lessThan') != None:
            for filter_name in filters['lessThan'].keys():
                if filters['lessThan'].get(filter_name) != None:
                    query = query.where(getattr(table.c, filter_name) <= '')
                    values[filter_name + '_1'] = filters['lessThan'].get(filter_name)

        if filters.get('greaterThan') != None:
            for filter_name in filters['greaterThan'].keys():
                if filters['greaterThan'].get(filter_name) != None:
                    query = query.where(getattr(table.c, filter_name) >= '')
                    values[filter_name + '_1'] = filters['greaterThan'].get(filter_name)

    if values == {}:
        values = None
    return query, values
