import os
import boto3
from botocore.exceptions import ClientError
import logging

from . callback_class import ProgressPercentage

def download_object(bucket_name: str, object_path: str, download_path: str = None):

    """Download a file from an S3 bucket

    :param bucket_name: Bucket to download from
    :param object_path: Path to the object to be downloaded
    :param download_path: Path to where the downloaded file should be saved
    :return: True if file downloaded successfully, else False
    """

    if download_path is None:
        download_path = os.path.basename(object_path)

    try:

        s3 = boto3.client('s3')

        # This removes the file name from the path so that we can create any directories that don't already exist.
        
        from pathlib import Path
        parts = Path(download_path).parts[:-1]
        folder_path = "/".join(parts)
        
        if folder_path:
            os.makedirs(folder_path, exist_ok=True)

        # Now that all necessary folders have been made, we can download the file to request location.
        s3.download_file(bucket_name, object_path, download_path)

    except ClientError as e:
        logging.error(e)
        return False
    
    return True
