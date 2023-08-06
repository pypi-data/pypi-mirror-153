## cs-models

This package provides a reusable library to connect to the cs database.

### Setup

1. Install the python version stated in `.python-version` using `pyenv`
2. Install invoke: `pip install invoke`
3. Install project dependencies: `inv install`

### Commands

**List commands**

`inv -l`

### Usage

**Configure the database in your app**

```
from silver_surfer_models.database import get_db_session

db_uri = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8mb4' % (
    'root',
    'password',
    'host',
    'db',
)
engine, db_session, Base = database.get_db_session(db_uri)

```

### How to release a new version?

**Update the `version` in `setup.py`**

```
setuptools.setup(
    ...
    version='0.0.9',
    ...
)
```

**Publish to PyPi repository**

```inv deploy```
