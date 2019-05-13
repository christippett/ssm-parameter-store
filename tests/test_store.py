import boto3
import pytest
from moto import mock_ssm

from ssm_parameter_store import EC2ParameterStore


@pytest.fixture
def fake_ssm():
    """Provide a consistent faked SSM context for running an entire test case."""
    with mock_ssm():
        yield None


@pytest.fixture
def parameter_store(fake_ssm):
    """An SSM parameter store with a well-known set of fake test data"""
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


def test_extract_parameter_returns_key_pair_tuple(parameter_store):
    parameter = {
        'Name': 'key',
        'Value': 'hello'
    }
    extracted_parameter = parameter_store.extract_parameter(parameter)
    assert isinstance(extracted_parameter, tuple)
    assert extracted_parameter[0] == 'key'
    assert extracted_parameter[1] == 'hello'


def test_get_paginated_parameters(parameter_store):
    """ SSM returns a maximum of 10 parameters per response
        - additional keys can be requested by passing
        NextToken in subsequent requests.
    """
    client_kwargs = dict(Path='/test/path/')
    parameter_keys = parameter_store._get_paginated_parameters(
        client_method=boto3.client('ssm').get_parameters_by_path,
        **client_kwargs
    )
    assert len(parameter_keys) == 20


def test_get_parameter(parameter_store):
    parameter_keys = parameter_store.get_parameter('key')
    assert len(parameter_keys) == 1
    assert 'key' in parameter_keys.keys()
    assert parameter_keys.get('key') == 'hello'


def test_get_parameters(parameter_store):
    parameter_keys = parameter_store.get_parameters(['key', 'second-key'])
    assert len(parameter_keys) == 2
    assert 'key' in parameter_keys.keys()
    assert 'second-key' in parameter_keys.keys()
    assert parameter_keys.get('key') == 'hello'
    assert parameter_keys.get('second-key') == 'world'


def test_get_parameters_by_path(parameter_store):
    parameter_keys = parameter_store.get_parameters_by_path('/path/to/another/key/')
    assert len(parameter_keys) == 1


def test_get_parameters_by_path_with_recursion(parameter_store):
    parameter_keys = parameter_store.get_parameters_by_path('/path/to/', recursive=True)
    assert len(parameter_keys) == 3


def test_get_parameters_by_path_without_recursion(parameter_store):
    parameter_keys = parameter_store.get_parameters_by_path('/path/to/', recursive=False)
    assert len(parameter_keys) == 2


def test_stripping_path_in_parameter(parameter_store):
    parameter_keys = parameter_store.get_parameter('/path/to/third-key', strip_path=False)
    assert parameter_keys.get('/path/to/third-key')

    stripped_parameter_keys = parameter_store.get_parameter('/path/to/third-key', strip_path=True)
    assert stripped_parameter_keys.get('third-key')

    stripped_parameter_keys = parameter_store.get_parameter('key', strip_path=True)
    assert stripped_parameter_keys.get('key')


def test_get_parameters_with_hierarchy(parameter_store):
    expected_result = {
        'third-key': 'danger',
        'fourth-key': 'will',
        'another': {
            'key': {
                'fifth-key': 'robinson',
            },
        },
    }

    parameter_keys = parameter_store.get_parameters_with_hierarchy('/path/to', strip_path=True)
    assert parameter_keys == expected_result

    parameter_keys = parameter_store.get_parameters_with_hierarchy('/path/to', strip_path=False)
    assert parameter_keys == {
        'path': {
            'to': expected_result,
        },
    }


def test_get_parameters_with_hierarchy_for_path_with_no_nesting(parameter_store):
    parameter_keys = parameter_store.get_parameters_with_hierarchy('/path/to/another/key/', strip_path=True)

    assert len(parameter_keys) == 1
    assert parameter_keys.get('fifth-key')


def test_get_parameters_with_hierarchy_for_nonexistent_path(parameter_store):
    parameter_keys = parameter_store.get_parameters_with_hierarchy('/does/not/exist', strip_path=True)
    assert len(parameter_keys) == 0
