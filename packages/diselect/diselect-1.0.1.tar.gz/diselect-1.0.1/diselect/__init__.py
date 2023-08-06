from .procedures import *



def diselect(container, query):
    '''query examples: 
        [field1, field2],
        {
            field1: alias1,
            field2: [alias2, func],
        }
        ex) diselect({('path1,', 'path2): ('alias', int)})
    '''
    norm_query = normalize_query(query)
    records = flatten_container(container)
    if selected := select_container(norm_query, records):
        selected = groupby_selected(selected)
        selected = transform_selected(norm_query, selected)
        return selected
    return []
