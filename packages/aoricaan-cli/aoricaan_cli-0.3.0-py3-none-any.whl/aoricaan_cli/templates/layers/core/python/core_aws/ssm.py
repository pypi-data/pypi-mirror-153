import json
import logging

import boto3
from botocore import exceptions
from core_utils.environment import ENVIRONMENT

__all__ = [
    "get_parameter"
]

LOGGER = logging.getLogger('layer-ssm')


def get_parameter(ssm_name, use_environ=True, default=None):
    """
    Request data from SSM service on AWS

    Args:
        ssm_name: Parameter name in SSM service
        use_environ: True if the parameter in SSM is an string like {parameter name}-{ENVIRONMENT}'
        default: Define the return default if not exist the parameter in SSM service

    Returns: Value for the param in SSM service if it exist else return value default.

    """
    try:
        ssm = boto3.client('ssm')
    except Exception as details:
        LOGGER.error('Error create client ssm')
        LOGGER.error('Details: {}'.format(details))
        raise exceptions.ClientError
    try:
        if use_environ:
            ssm_name = f'{ssm_name}-{ENVIRONMENT}'
        parameters = ssm.get_parameter(Name=ssm_name)['Parameter']['Value']
    except Exception as details:
        LOGGER.warning(details)
        return default
    else:
        LOGGER.debug(f'Value for {ssm_name}: {parameters}')
        parameters = json.loads(parameters)
        return parameters
