# python-geoacumen

## Installation

```
pip install python-geoacumen
```

## Usage

```
>>> import geoacumen
>>> import maxminddb
>>> reader = maxminddb.open_database(geoacumen.db_path)
>>> reader.get("1.1.1.1")
{'country': {'iso_code': 'CN'}}
>>>
```