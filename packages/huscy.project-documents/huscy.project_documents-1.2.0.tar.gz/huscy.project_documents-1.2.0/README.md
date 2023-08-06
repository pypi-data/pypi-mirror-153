huscy.project_documents
======

![PyPi Version](https://img.shields.io/pypi/v/huscy-project_documents.svg)
![PyPi Status](https://img.shields.io/pypi/status/huscy-project_documents)
![PyPI Downloads](https://img.shields.io/pypi/dm/huscy-project_documents)
![PyPI License](https://img.shields.io/pypi/l/huscy-project_documents?color=yellow)
![Python Versions](https://img.shields.io/pypi/pyversions/huscy-project_documents.svg)
![Django Versions](https://img.shields.io/pypi/djversions/huscy-project_documents)



Requirements
------

- Python 3.6+
- A supported version of Django

Tox tests on Django versions 3.2 and 4.0.



Installation
------

To install `husy.project_documents` simply run:
```
pip install huscy.project_documents
```



Configuration
------

We need to hook `huscy.project_documents` into our project.
This package depends on `huscy.projects` so we have to add this as well.
We also have to add further requirements for django_guardian, django_restframework and drf_nested_routers.

1. Add packages into your `INSTALLED_APPS` at settings module:

```python
INSTALLED_APPS = (
    ...
    'guardian',
    'rest_framework',
    'rest_framework_nested',

    'huscy.project_documents',
    'huscy.projects',
)
```

2. Create `huscy.project_documents` database tables by running:

```
python manage.py migrate
```


Development
------

After checking out the repository you should run

```
make install
```

to install all development and test requirements and

```
make migrate
```

to create the database tables.
We assume you have a running postgres database with a user `huscy` and a database also called `huscy`.
You can easily create them by running

```
sudo -u postgres createdb huscy
sudo -u postgres createuser -d huscy
sudo -u postgres psql -c "ALTER USER huscy WITH PASSWORD '123'"
sudo -u postgres psql -c "ALTER DATABASE huscy OWNER TO huscy;"
```
