SSM Parameter Store
=============================================================

[![PyPI version](https://img.shields.io/pypi/v/ssm-parameter-store.svg)](https://pypi.python.org/pypi/ssm-parameter-store)
[![Build status](https://img.shields.io/travis/christippett/ssm-parameter-store.svg)](https://travis-ci.org/christippett/ssm-parameter-store)
[![Coverage](https://img.shields.io/coveralls/github/christippett/ssm-parameter-store.svg)](https://coveralls.io/github/christippett/ssm-parameter-store?branch=master)
[![Python versions](https://img.shields.io/pypi/pyversions/ssm-parameter-store.svg)](https://pypi.python.org/pypi/ssm-parameter-store)
[![Github license](https://img.shields.io/github/license/christippett/ssm-parameter-store.svg)](https://github.com/christippett/ssm-parameter-store)

Description
===========

This is a simple Python wrapper for getting values from AWS Systems Manager
Parameter Store.

The module supports getting a single parameter, multiple parameters or all parameters matching a particular path.

All parameters are returned as a Python `dict`.

Installation
============

Install with `pip`:

``` bash
pip install ssm-parameter-store
```

Usage
=====

Import the module and create a new instance of `EC2ParameterStore`.

```python
from ssm_parameter_store import EC2ParameterStore

store = EC2ParameterStore()
```

AWS Credentials
---------------

`ssm-parameter-store` uses `boto3` under the hood and therefore inherits
the same mechanism for looking up AWS credentials. See [configuring
credentials](https://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials)
in the Boto 3 documentation for more information.

`EC2ParameterStore` accepts all `boto3` client parameters as keyword arguments.

For example:

``` python
from ssm_parameter_store import EC2ParameterStore

store = EC2ParameterStore(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN,  # optional
    region_name='us-west-2'
)
```

Examples
========

Given the following parameters:

``` bash
# set default AWS region
AWS_DEFAULT_REGION=us-west-2

# add parameters
aws ssm put-parameter --name "param1" --value "value1" --type SecureString
aws ssm put-parameter --name "param2" --value "value2" --type SecureString

# add parameters organised by hierarchy
aws ssm put-parameter --name "/dev/app/secret" --value "dev_secret" --type SecureString
aws ssm put-parameter --name "/dev/db/postgres_username" --value "dev_username" --type SecureString
aws ssm put-parameter --name "/dev/db/postgres_password" --value "dev_password" --type SecureString
aws ssm put-parameter --name "/prod/app/secret" --value "prod_secret" --type SecureString
aws ssm put-parameter --name "/prod/db/postgres_username" --value "prod_username" --type SecureString
aws ssm put-parameter --name "/prod/db/postgres_password" --value "prod_password" --type SecureString
```


Get a single parameter
----------------------

``` python
parameter = store.get_parameter('param1', decrypt=True)

assert parameter == {
   'param1': 'value1'
}
```

Get multiple parameters
-----------------------

``` python
parameters = store.get_parameters(['param1', 'param2'])

assert parameters == {
   'param1': 'value1',
   'param2': 'value2',
}
```

Get parameters by path
----------------------

``` python
parameters = store.get_parameters_by_path('/dev/', recursive=True)

assert parameters == {
    'secret': 'dev_secret',
    'postgres_username': 'dev_username',
    'postgres_password': 'dev_password',
}
```

By default `get_parameters_by_path` strips the path from each parameter name. To return a parameter's full name, set `strip_path` to `False`.

``` python
parameters = store.get_parameters_by_path('/dev/', strip_path=False, recursive=True)

assert parameters == {
    '/dev/app/secret': 'dev_secret',
    '/dev/db/postgres_username': 'dev_username',
    '/dev/db/postgres_password': 'dev_password'
}
```

Get parameters with original hierarchy
--------------------------------------
You can also get parameters by path, but in a nested structure that models the path hierarchy.

``` python
parameters = store.get_parameters_with_hierarchy('/dev/')

assert parameters == {
    'app': {
        'secret': 'dev_secret',
    },
    'db': {
        'postgres_username': 'dev_username',
        'postgres_password': 'dev_password',
    },
}
```

By default `get_parameters_with_hierarchy` strips the leading path component. To return the selected parameters
with the full hierarchy, set `strip_path` to `False`.

``` python
parameters = store.get_parameters_with_hierarchy('/dev/', strip_path=False)

assert parameters == {
    'dev': {
        'app': {
            'secret': 'dev_secret',
        },
        'db': {
            'postgres_username': 'dev_username',
            'postgres_password': 'dev_password',
        },
    },
}
```


Populating Environment Variables
================================

The module includes a static method on `EC2ParameterStore` to help populate environment variables. This can be helpful when integrating with a library like [`django-environ`](https://github.com/joke2k/django-environ).

Example
-------
Given the following parameters:

```bash
aws ssm put-parameter --name "/prod/django/SECRET_KEY" --value "-$y_^@69bm69+z!fawbdf=h_10+zjzfwr8_c=$$&j@-%p$%ct^" --type SecureString
aws ssm put-parameter --name "/prod/django/DATABASE_URL" --value "psql://user:pass@db-prod.xyz123.us-west-2.rds.amazonaws.com:5432/db" --type SecureString
aws ssm put-parameter --name "/prod/django/REDIS_URL" --value "redis://redis-prod.edc1ba.0001.usw2.cache.amazonaws.com:6379" --type SecureString
```

```python
import environ
from ssm_parameter_store import EC2ParameterStore

env = environ.Env(
    DEBUG=(bool, False)
)

# Get parameters and populate os.environ (region not required if AWS_DEFAULT_REGION environment variable set)
parameter_store = EC2ParameterStore(region_name='us-west-2')
django_parameters = parameter_store.get_parameters_by_path('/prod/django/', strip_path=True)
EC2ParameterStore.set_env(django_parameters)

# False if not in os.environ
DEBUG = env('DEBUG')

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db(),
}

CACHES = {
    'default': env.cache('REDIS_URL'),
}
```

Related Projects
================

- **[param-store](https://github.com/LabD/python-param-store)** – 
Python module to store secrets in secret stores
- **[ssm-cache](https://github.com/alexcasalboni/ssm-cache-python)** –
AWS System Manager Parameter Store caching client for Python

