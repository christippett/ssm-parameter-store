Simple Python wrapper for getting values from AWS Systems Manager Parameter Store
=============================================================

.. image:: https://img.shields.io/travis/christippett/ssm-parameter-store.svg
    :target: https://travis-ci.org/christippett/ssm-parameter-store

.. image:: https://img.shields.io/coveralls/github/christippett/ssm-parameter-store.svg
    :target: https://coveralls.io/github/christippett/ssm-parameter-store?branch=master

.. image:: https://img.shields.io/github/license/christippett/ssm-parameter-store.svg
    :target: https://github.com/christippett/ssm-parameter-store

.. image:: https://img.shields.io/pypi/pyversions/ssm-parameter-store.svg
    :target: https://pypi.python.org/pypi/ssm-parameter-store


Installation
------------

Install the module with ``pip``:

.. code:: bash

   pip install ssm-parameter-store

Usage
-----

All parameters are returned as a Python ``dict``.

Getting a single parameter
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   aws ssm put-parameter \
   --name "my_parameter_name" \
   --value "value" \
   --type SecureString
   --region us-west-2

.. code:: python

   from ssm_parameter_store import EC2ParameterStore
   store = EC2ParameterStore(region='us-west-2')
   parameter = store.get_parameter('my_parameter_name', decrypt=True)
   # parameter = {
   #   'my_parameter_name': 'value'
   # }

Credentials
-----------

``ssm-parameter-store`` uses ``boto3`` under the hood and therefore
inherits the same mechanism for looking up AWS credentials. See
`configuring credentials <https://boto3.readthedocs.io/en/latest/guide/configuration.html#configuring-credentials>`__
in the Boto 3 documentation for more information.

Example: Method parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~

Pass all ``boto3`` client parameters to the ``EC2ParameterStore``
constructor.

.. code:: python

   from ssm_parameter_store import EC2ParameterStore
   store = EC2ParameterStore(
       aws_access_key_id=ACCESS_KEY,
       aws_secret_access_key=SECRET_KEY,
       aws_session_token=SESSION_TOKEN,  # optional
       region='us-west-2'
   )
