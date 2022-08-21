import logging
import boto3
from botocore.exceptions import ClientError


def create_presigned_url(object_name, bucket_name = None, expiration=3600):

    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Check environment variables for bucket name
    if bucket_name is None:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        bucket_name = os.environ.get('S3_BUCKET_NAME')

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response
