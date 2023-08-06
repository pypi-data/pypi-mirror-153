from itertools import groupby



def normalize_query(query):
    if isinstance(query, dict):
        query = [query]
    qs = {}
    for qry in query:
        if isinstance(qry, dict):
            for q, rest in qry.items():
                if isinstance(q, str):
                    q = q,
                if isinstance(rest, (list, tuple)) and len(rest) == 2:
                    alias, apply = rest
                elif isinstance(rest, str):
                    alias, apply = rest, lambda x:x
                else:
                    raise ValueError(f'Invalid Query Value: {q}')
                qs[q] = (alias, apply)
        elif isinstance(qry, (tuple, list)):
            qs[qry] = (qry, lambda x:x)
        elif isinstance(qry, str):
            qs[(qry,)] = (qry, lambda x:x)
        else:
            raise ValueError('Invalid Query Key')
    return qs


def flatten_container(container):
    '''inspect index, path, value
    '''
    cntrq = [((), (0,), container)]
    ret = []
    while cntrq:
        path, index, cntr = cntrq.pop(0)
        p = None
        if isinstance(cntr, dict):
            for key, value in cntr.items():
                p = *path, key,
                cntrq.append((p, index, value))
        
        elif isinstance(cntr, (list, tuple, set)):
            for i, c in enumerate(cntr):
                idx = *index, i
                cntrq.append((path, idx, c))
        else:
            ret.append((index, path, cntr))
    return ret


def select_container(norm_query, flatten):
    
    def query_match(path, query):
        if len(query) > len(path):
            return False
        return path[-len(query):] == query

    queries = norm_query.keys()

    selected = []
    match_cases = {}
    for index, path, value in flatten:
        for query in queries:
            if query_match(path, query):
                match_cases.setdefault(query, set()).add(path)
                selected.append((index, path, query, value))

    over_matched = {
       k:v for k, v in match_cases.items() if len(v) > 1
    }

    if under_matched := (queries - match_cases.keys()):
        print(f'diselect Warning: Cannot find path of {under_matched}')

    if over_matched:
        raise KeyError(f'matched at muliteple path of items, Use more detail query of path {over_matched}')

    if not selected:
        print(f'diselect Warning: Queries has empthy results')
    return selected


def groupby_selected(selected):

    def get_common_index_length(selected):
        return min([
            len(index) for index, path, query, value in selected
        ])
    
    selected = list(sorted(selected, key=lambda sel: sel[0]))
    
    common_index_length = get_common_index_length(selected)

    for name, grouped in groupby(selected, key=lambda sel: sel[0][:common_index_length]):
        select = {}
        for sel in grouped:
            index, path, query, value = sel
            if len(index) == common_index_length:
                select.update({query: value})
            elif len(index) > common_index_length:
                select.setdefault(query, []).append(value)
        yield select


def transform_selected(norm_query, selected):
    # ordering
    quries = list(norm_query.keys())
    selected = [
        {q:sel[q] for q in quries if q in sel}
        for sel in selected
    ]
    #aliasing
    for select in selected:
        transformed = {}
        for qry, val in select.items():
            alias, apply = norm_query[qry]
            try:
                transformed[alias] = apply(val)
            except Exception as e:
                transformed[alias] = val
                print(f'diselect Warning: apply function for value has failed due to{e}, return to original value:{val}')
        yield transformed


    