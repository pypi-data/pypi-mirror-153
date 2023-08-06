## 1. Introduction
### - A smart and convenience single function for extracting container value consisting of list and dict
### - Query a container with a complex structure, mainly generated from json, and flatten it into a dict with a single structure.
### - Get freedom from code that indexes complex json data one by one and writes for loops like this below...
> 
```python

# extracting from json loads data..

sample_from_json = json.loads('sample.json')

count = sample_from_json['count']
data_list = sample_from_json.get('data_list')

for cityinfo in data_list:
    for key, value in cityinfo.items():
        if key == 'city':
            city_name = value['names']['en']
        if key == 'subdivisions':
            subdiv = []
            for subsubdivision in value:
                sv = subsubdivision['names']['en']
                subdiv.append(sv)
                ...
                ...
            ...
        ...
        ...
    ...
    ...
    OMG...
    ...
    forif Hell...
    ....
```
---

## 2. Installation and Usage
 - Made in Python 3.8 or later
```shell
pip install diselect
```
```python
from diselect import diselect

# example
# list of dict in dict in list in dict in list of dict in....
sample_from_json = {
    'count': 1,
    'date': '2022-5-31',
    'data_list': [
        {
            "city": {
                "names": {
                    "en": "Songpa-gu"
                }
            },
            "continent": {
                "code": "AS",
                "names": {"pt-BR": "Ásia", "de": "Asien", "en": "Asia",}
            },
            "country": {
                "iso_code": "KR", 
                "names": {
                    "de": "Südkorea",
                    "en": "South Korea",
                }
            },
            "location": {"latitude": 37.5013, "longitude": 127.1188, "time_zone": "Asia/Seoul"},

            # multiple childerns of list
            "subdivisions": [
                {
                    "iso_code": "11",
                    "names": {"zh-CN": "首尔特别市", "en": "Seoul", "ja": "ソウル特別市"}
                },
                {
                    "iso_code": "12",
                    "names": {"en": "Hangang"}
                }
            ],
            
        },
        {
            "city": {
                "names": {
                    "en": "Songpa-gu2"
                }
            },
            "continent": {
                "code": "AS2",
                "names": {"pt-BR": "Ásia2", "de": "Asien", "en": "Asia2",}
            },
            "country": {
                "iso_code": "KR2", 
                "names": {
                    "de": "Südkorea2",
                    "en": "South Korea2",
                }
            },
            "location": {"latitude": 37.5013, "longitude": 127.1188, "time_zone": "Asia/Seoul2"},

            # multiple childerns of list
            "subdivisions": [
                {
                    "iso_code": "112",
                    "names": {"zh-CN": "首尔特别市", "en": "Seoul2", "ja": "ソウル特別市"}
                },
                {
                    "iso_code": "122",
                    "names": {"en": "Hangang2"}
                }
            ],
            
        },
    ]
}


```
```python
# Useage 1) Specify only the column name
# When taking the highest values in container ​​without the risk of duplication

query_only_key = ['count', 'date'] # key name to column
for r in diselect(sample_from_json, query_only_key):
    print(r)

# results {'count': 1, 'date': '2022-5-31'}
```

```python
# Useage 2) Extract nested values
# parent paths tuple keys of target 'terminal' value
# If there are few parental generations, duplicate matching may occur.
# Exception when duplicate occurs

query_deep_path = [('city', 'names', 'en'), ('country', 'names', 'en')] # en is key of terminal value
for r in diselect(sample_from_json, query_deep_path):
    print(r)

# results 
# {('city', 'names', 'en'): 'Songpa-gu', ('country', 'names', 'en'): 'South Korea'}
# {('city', 'names', 'en'): 'Songpa-gu2', ('country', 'names', 'en'): 'South Korea2'}
```

```python
# Useage 3) Aliasing query to column name
# Change the query to an usable column name

query_aliases = {
    ('city', 'names', 'en'): 'city_name',
    ('country', 'names', 'en'): 'country_name',
    ('subdivisions', 'names', 'en'): 'subdivision_name'
}
# or
query_aliases = [
    {('city', 'names', 'en'): 'city_name'},
    {('country', 'names', 'en'): 'country_name'},
    {('subdivisions', 'names', 'en'): 'subdivision_names'}
]

for r in diselect(sample_from_json, query_aliases):
    print(r)

# results:
# {'city_name': 'Songpa-gu', 'country_name': 'South Korea', 'subdivision_names': ['Seoul', 'Hangang']}
# {'city_name': 'Songpa-gu2', 'country_name': 'South Korea2', 'subdivision_names': ['Seoul2', 'Hangang2']}
# multiple children values of subdivision_names has coaleased to list ['Seoul', 'Hangang']
```
```python
# Useage 4) join listed children values
# pass tuple value of aliase and function 

query_aliases_and_join_children = {
    ('city', 'names', 'en'): 'city_name',
    ('country', 'names', 'en'): 'country_name',
    ('subdivisions', 'names', 'en'): ('subdivision_names', ','.join), # alias, str join function
}

for r in diselect(sample_from_json, query_aliases_and_join_children):
    print(r)

# results
# {'city_name': 'Songpa-gu', 'country_name': 'South Korea', 'subdivision_names': 'Seoul,Hangang'}
# {'city_name': 'Songpa-gu2', 'country_name': 'South Korea2', 'subdivision_names': 'Seoul2,Hangang2'}
# Soule, Hangang has joined with sep ','
```

```python
# 4) Summary
query = {
    ('city', 'names', 'en'): 'city_name',
    ('continent', 'code'): 'continent_code',
    ('continent', 'names', 'en'): 'continent_name',
    ('country', 'iso_code'): 'country_code',
    ('country', 'names', 'en'): 'country_name',
    ('location', 'time_zone'): 'timezone',
    ('subdivisions', 'names', 'en'): ('subdivision_name', '|'.join), 
}

for r in diselect(container=sample_from_json, query=query):
    print(r)

# results
# {'city_name': 'Songpa-gu', 'continent_code': 'AS', 'continent_name': 'Asia', 'country_code': 'KR', 'country_name': 'South Korea', 'timezone': 'Asia/Seoul', 'subdivision_name': 'Seoul,Hangang'}
# {'city_name': 'Songpa-gu2', 'continent_code': 'AS2', 'continent_name': 'Asia2', 'country_code': 'KR2', 'country_name': 'South Korea2', 'timezone': 'Asia/Seoul2', 'subdivision_name': 'Seoul2,Hangang2'}
```

----

## 3. Arguments
### 1. container
    > nested with dict and list complex data
### 2. query
```python
query1 = {
    key1, key2,
    {(key3, key2): alias},
    {(key4, key5): (alias2, apply)},
}
query2 = [
    'column1', 'column2',
    {
        ('path1', 'path2'): 'alias1',
        ('patt1', 'path2', 'path3'): ('alias2', dateutil.parser.parse),
    },
    'column4'
]
```
- non-overlapping 'minimum' path of value item (need not be fullpath)
- parents path lists key of target 'terminal' value (target value must be scalar value, like str, int...)
- More detail is better to avoid duplication (...great-grandparent, grandparent, parent)
- You can mix dict and tuple
- The results column order of the output matches the order of the query
- alias: column name representing the query
- apply: function to be applied to value
### 3. caution
- If there is no query matching the key path of the container, a warning is output and it does not appear into the result column.
- If the matching of the query is duplicated, an exception is raised and a more detailed query is requested.
- Consider the data structure of the container. Suggested queries are aggregated by matching top-level keys of matched with query.
```python
# date and count in the presented example data are single entities as top-level keys.
  # 'count': 1,
  # 'date': '2022-5-31',
  # 'data_list': [ ...
# but data_list is multiple row value
# Querying data from both tendencies at the same time leads to unpredictable behavior.

greedy_query = [
    # query for top level single context value
    'count', 'date', 
    # query for row values
    {
        ('city', 'names', 'en'): 'city_name',
        ('continent', 'code'): 'continent_code',
        ('continent', 'names', 'en'): 'continent_name',
        ('country', 'iso_code'): 'country_code',
        ('country', 'names', 'en'): 'country_name',
        ('location', 'time_zone'): 'timezone',
        ('subdivisions', 'names', 'en'): ('subdivision_name', ','.join), 
    }
]

for r in diselect(sample_from_json, greedy_query):
    print(r)

# results
# {'count': 1, 'date': '2022-5-31', 'city_name': ['Songpa-gu', 'Songpa-gu2'], 'continent_code': ['AS', 'AS2'], 'continent_name': ['Asia', 'Asia2'], 'country_code': ['KR', 'KR2'], 'country_name': ['South Korea', 'South Korea2'], 'timezone': ['Asia/Seoul', 'Asia/Seoul2'], 'subdivision_name': 'Seoul,Hangang,Seoul2,Hangang2'}

# The data is organized vertically with the top keys count and date. Maybe this is what you want.
# This can be used as a trick to get the column dataset


## Tip. separate query by structure for get two of them both
query_context = ['count', 'date']

query_list = {
    ('city', 'names', 'en'): 'city_name',
    ('continent', 'code'): 'continent_code',
    ('continent', 'names', 'en'): 'continent_name',
    ('country', 'iso_code'): 'country_code',
    ('country', 'names', 'en'): 'country_name',
    ('location', 'time_zone'): 'timezone',
    ('subdivisions', 'names', 'en'): ('subdivision_name', ','.join), 
}



[context_data] = list(diselect(sample_from_json, query_context)) # may one
count = context_data['count']
date = context_data['date']

# or may be simple and better just direct indexing when values are easy to access
count = sample_from_json['count']
date = sample_from_json['date']

data_list = list(diselect(sample_from_json, query_list)) # many

```

## 4. More Useages

### 1. typing values
    - value typing via apply function

```python
import dateutil

data = [
    {
        'place_id': 142213,
        'visit_count': '5',
        'visit_date': '2022/2/21',
        'rating': '2.5',
    },
    {
        'place_id': 154321,
        'visit_count': '12',
        'visit_date': '2022.3.7.',
        'rating': '4.5',
    },
]

parsed = diselect(data,
{
    'place_id': ('place_id', str),
    'visit_count': ('visit_count', int),
    'rating': ('point', float),
    'visit_date': ('visit_count', dateutil.parser.parse),
})
for row in parsed:
    print(row)
# results
# {'place_id': '142213', 'visit_count': datetime.datetime(2022, 2, 21, 0, 0), 'point': 2.5}
# {'place_id': '154321', 'visit_count': datetime.datetime(2022, 3, 7, 0, 0), 'point': 4.5}
```
