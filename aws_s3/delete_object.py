import boto3


def delete_object(bucket_name, object_path):

    s3 = boto3.resource('s3')

    s3_object = s3.Object(bucket_name, object_path)

    response = s3_object.delete()


def delete_folder(bucket_name, folder_path):

    s3 = boto3.resource('s3')

    s3_bucket = s3.Bucket(bucket_name)

    if folder_path[-1] != '/':
        folder_path += '/'

    print('Folder path:', folder_path)

    response = s3_bucket.objects.filter(Prefix=folder_path).delete()
