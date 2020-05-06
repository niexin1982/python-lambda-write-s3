"""app/lambda_function.py
"""

import os
import sys
from datetime import datetime, timedelta, timezone

from boto3.session import Session


def _localtime(time_zone):
    """_localtime
    """
    return datetime.now(timezone.utc)+timedelta(hours=int(time_zone))


def _write_to_s3(param):
    """_write_to_s3
    """
    access_key_id = param.get('aws_access_key_id')
    secret_access_key = param.get('aws_secret_access_key')
    region_name = param.get('aws_region_name')
    bucket_name = param.get('s3_bucket_name')
    file_name_format = param.get('s3_file_name_format')
    encode = param.get('s3_encode')
    data = param.get('data')

    session = Session(aws_access_key_id=access_key_id,
                      aws_secret_access_key=secret_access_key,
                      region_name=region_name)
    s3 = session.resource('s3')
    bucket = s3.Bucket(bucket_name)  # pylint: disable=no-member

    fname = '{}.csv'.format(_localtime(time_zone=9).strftime(file_name_format))
    print('fname: {}'.format(fname))
    obj = bucket.Object(fname)

    try:
        obj.put(
            Body=data.encode(encode, 'ignore'),
            ContentEncoding=encode,
            ContentType='text/csv'
        )
    except AttributeError as e:
        print(e)
        sys.exit()


def lambda_handler(event, context):
    """lambda_handler
    """
    print('event: {}'.format(event))
    print('context: {}'.format(context))

    param = {
        'aws_access_key_id': os.getenv('S3_ACCESS_KEY_ID', ''),
        'aws_secret_access_key': os.getenv('S3_SECRET_ACCESS_KEY', ''),
        'aws_region_name': os.getenv('S3_REGION_NAME', ''),
        's3_bucket_name': os.getenv('S3_BUCKET_NAME', ''),
        's3_file_name_format': os.getenv('S3_FILE_NAME_FORMAT', ''),
        's3_encode': os.getenv('S3_ENCODE', ''),
        'data': _localtime(time_zone=0).strftime('%Y-%m-%dT%H:%M:%S+00:00')
    }
    _write_to_s3(param=param)

    return {
        'status_code': 200
    }


if __name__ == '__main__':
    lambda_handler(event=None, context=None)
