import logging
import boto3
from botocore.exceptions import ClientError
import os

from . callback_class import ProgressPercentage

def upload_file(file_path, bucket, object_path=None):

    """Upload a file to an S3 bucket

    :param file_path: File to upload
    :param bucket: Bucket to upload to
    :param object_path: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_path is None:
        object_path = os.path.basename(file_path)

    # Upload the file
    s3_client = boto3.client('s3')
    
    try:
        response = s3_client.upload_file(
            file_path, bucket, object_path,
            Callback=ProgressPercentage(file_path))
    
    except ClientError as e:
        logging.error(e)
        return False
    
    return True
