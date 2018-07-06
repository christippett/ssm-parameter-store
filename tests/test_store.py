import boto3
import pytest
from moto import mock_ssm

from ssm_parameter_store import EC2ParameterStore


@pytest.fixture
def parameter_store():
    # Load test parameters
    ssm = boto3.client('ssm')
    ssm.put_parameter(Name='key', Value='hello', Type='SecureString')
    ssm.put_parameter(Name='second-key', Value='world', Type='String')
    ssm.put_parameter(Name='/path/to/third-key', Value='danger', Type='SecureString')
    ssm.put_parameter(Name='/path/to/fourth-key', Value='will', Type='SecureString')
    ssm.put_parameter(Name='/path/to/another/key/fifth-key', Value='robinson', Type='String')
    # Generate more than 10 parameters to test limit of 10 parameters per response
    for n in range(0, 20):
        ssm.put_parameter(Name='/test/path/{}'.format(n), Value='{}'.format(n), Type='SecureString')
    return EC2ParameterStore()


@mock_ssm
def test_extract_parameter_returns_key_pair_tuple():
    store = parameter_store()
    parameter = {
        'Name': 'key',
        'Value': 'hello'
    }
    extracted_parameter = store.extract_parameter(parameter)
    assert isinstance(extracted_parameter, tuple)
    assert extracted_parameter[0] == 'key'
    assert extracted_parameter[1] == 'hello'


@mock_ssm
def test_get_paginated_parameters():
    """ SSM returns a maximum of 10 parameters per response
        - additional keys can be requested by passing
        NextToken in subsequent requests.
    """
    store = parameter_store()
    client_kwargs = dict(Path='/test/path/')
    parameter_keys = store._get_paginated_parameters(
        client_method=boto3.client('ssm').get_parameters_by_path,
        **client_kwargs
    )
    assert len(parameter_keys) == 20


@mock_ssm
def test_get_parameter():
    store = parameter_store()
    parameter_keys = store.get_parameter('key')
    assert len(parameter_keys) == 1
    assert 'key' in parameter_keys.keys()
    assert parameter_keys.get('key') == 'hello'


@mock_ssm
def test_get_parameters():
    store = parameter_store()
    parameter_keys = store.get_parameters(['key', 'second-key'])
    assert len(parameter_keys) == 2
    assert 'key' in parameter_keys.keys()
    assert 'second-key' in parameter_keys.keys()
    assert parameter_keys.get('key') == 'hello'
    assert parameter_keys.get('second-key') == 'world'


@mock_ssm
def test_get_parameters_by_path():
    store = parameter_store()
    parameter_keys = store.get_parameters_by_path('/path/to/another/key/')
    assert len(parameter_keys) == 1


@mock_ssm
def test_get_parameters_by_path_with_recursion():
    store = parameter_store()
    parameter_keys = store.get_parameters_by_path('/path/to/', recursive=True)
    assert len(parameter_keys) == 3


@mock_ssm
def test_get_parameters_by_path_without_recursion():
    store = parameter_store()
    parameter_keys = store.get_parameters_by_path('/path/to/', recursive=False)
    assert len(parameter_keys) == 2


@mock_ssm
def test_stripping_path_in_parameter():
    store = parameter_store()
    parameter_keys = store.get_parameter('/path/to/third-key', strip_path=False)
    assert parameter_keys.get('/path/to/third-key')

    stripped_parameter_keys = store.get_parameter('/path/to/third-key', strip_path=True)
    assert stripped_parameter_keys.get('third-key')

    stripped_parameter_keys = store.get_parameter('key', strip_path=True)
    assert stripped_parameter_keys.get('key')

