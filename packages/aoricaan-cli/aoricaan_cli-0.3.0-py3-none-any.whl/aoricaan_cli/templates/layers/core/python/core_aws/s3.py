import logging
import os

import boto3
from botocore.exceptions import ClientError


__all__ = [
    "upload_file"
]

s3 = boto3.client('s3')


def upload_file(*, file_name, bucket, object_name=None):
    if not object_name:
        object_name = os.path.basename(file_name)

    try:
        response = s3.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    logging.debug(str(response))
    return True
