from notebooks.dao import *

from sqlalchemy import asc, desc, nullslast, nullsfirst


# sorts = [{'model':'Card', 'field': 'level', 'direction': 'des', 'nulls': 'nullslast'}]    
# filters = [{'model':'Card', 'field': 'level', 'op': '>=', 'value': 3}]

def apply_sort(query, sorts):
    if sorts is None:
        return query
    for sor in sorts:
        s = f"{sor['model']}.{sor['field']}" if sor.get('model') else sor['field']
        if sor['direction']:
            s = f"{sor['direction']}({s})"
        if sor['nulls']:
            s = f"{sor['nulls']}({s})"
        query = query.order_by(eval(s))
    return query


def apply_filter(query, filters):
    if filters is None:
        return query
    for fil in filters:
        field = f"{fil['model']}.{fil['field']}" if fil.get('model') else fil['field']
        s = f"{field} {fil['op']} {fil['value']}"
        query = query.filter(eval(s))
    return query