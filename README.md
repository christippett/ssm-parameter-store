Simple Python wrapper for getting values from AWS Systems Manager
Parameter Store
=============================================================

[![Build status](https://img.shields.io/travis/christippett/ssm-parameter-store.svg)](https://travis-ci.org/christippett/ssm-parameter-store)
[![Coverage](https://img.shields.io/coveralls/github/christippett/ssm-parameter-store.svg)](https://coveralls.io/github/christippett/ssm-parameter-store?branch=master)
[![Github license](https://img.shields.io/github/license/christippett/ssm-parameter-store.svg)](https://github.com/christippett/ssm-parameter-store)
[![Python versions](https://img.shields.io/pypi/pyversions/ssm-parameter-store.svg)](https://pypi.python.org/pypi/ssm-parameter-store)

Installation
============

Install the module with `pip`:

``` bash
pip install ssm-parameter-store
```

Usage
=====

All parameters are returned as a Python `dict`.

Getting a single parameter
--------------------------

``` bash
aws ssm put-parameter \
--name "my_parameter_name" \
--value "value" \
--type SecureString
--region us-west-2
```

``` python
from ssm_parameter_store import EC2ParameterStore
store = EC2ParameterStore(region='us-west-2')
parameter = store.get_parameter('my_parameter_name', decrypt=True)
# parameter = {
#   'my_parameter_name': 'value'
# }
```

Credentials
===========

`ssm-parameter-store` uses `boto3` under the hood and therefore inherits
the same mechanism for looking up AWS credentials. See [configuring
credentials](https://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials)
in the Boto 3 documentation for more information.

Example: Method parameters
--------------------------

Pass all `boto3` client parameters to the `EC2ParameterStore`
constructor.

``` python
from ssm_parameter_store import EC2ParameterStore
store = EC2ParameterStore(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN,  # optional
    region='us-west-2'
)
```
