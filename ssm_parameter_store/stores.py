import os
import logging

import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)


class EC2ParameterStore:
    def __init__(self, path_delimiter='/'):
        self.client = boto3.client('ssm')
        self.path_delimiter = path_delimiter

    @classmethod
    def set_env(cls, parameter_dict):
        for k, v in parameter_dict.items():
            os.environ.setdefault(k, v)

    def _extract_parameter(self, parameter):
        name = parameter['Name']
        name_parts = name.split(self.path_delimiter)
        key = name_parts[-1]
        value = parameter['Value']
        return (key, value)

    def get_parameter(self, name, decrypt=True):
        result = self.client.get_parameter(Name=name, WithDecryption=decrypt)
        p = result['Parameter']
        return dict([self._extract_parameter(p)])

    def get_parameters_by_path(self, path, decrypt=True, recursive=True):
        next_token = None
        client_kwargs = dict(Path=path, WithDecryption=decrypt, Recursive=recursive)
        parameters = []
        while True:
            result = self.client.get_parameters_by_path(**client_kwargs)
            parameters += result.get('Parameters')
            next_token = result.get('NextToken')
            if next_token is None:
                break
            client_kwargs.update({'NextToken': next_token})
        return dict(self._extract_parameter(p) for p in parameters)


if __name__ == '__main__':
    store = EC2ParameterStore()
    parameters = store.get_parameters_by_path(path='/aeroster/common')
    print(json.dumps(parameters))
    EC2ParameterStore.set_env(parameters)
    # print(os.environ.get('MAILGUN_API_KEY'))
    # print(store.get_parameter('/aeroster/common/AWS_S3_CUSTOM_DOMAIN'))
