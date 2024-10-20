import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import uuid
from datetime import datetime
import requests

# AWS 访问密钥
ACCESS_KEY = 'change to your key' #change to your key
SECRET_KEY = 'change to your key' #change to your key

# 创建 S3 客户端
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, region_name='us-east-1')

# 创建一个新的 S3 bucket
bucket_name = 'aigface'


def upload_file_to_s3(file, file_key, bucket_name='aigface'):
    """
    Upload a file to S3 and return the file URL.

    :param file: File-like object to upload.
    :param file_key: The key (path) where the file will be stored in S3.
    :return: The URL of the uploaded file.
    :raises Exception: If there's an error during upload.
    """
    try:
        s3.upload_fileobj(file, bucket_name, file_key)
        return f"https://{bucket_name}.s3.amazonaws.com/{file_key}"
    except NoCredentialsError:
        raise Exception("Credentials not available")
    except ClientError as e:
        raise Exception(f"Client error: {e}")
    except Exception as e:
        raise Exception(f"Error uploading file: {e}")
    
def gen_s3_filename(file_extension, user_id=None, folder_name='headshots/'):
    # Generate a unique filename using UUID
    unique_id = uuid.uuid4()
    # Optional: add user ID or other metadata in the file path
    today = datetime.now().strftime('%Y/%m/%d')
    # Construct the full path: folder_name/user_id/date/uuid.extension
    if user_id:
        s3_file_key = f"{folder_name}user_{user_id}/{today}/{unique_id}{file_extension}"
    else:
        s3_file_key = f"{folder_name}{today}/{unique_id}{file_extension}"
    return s3_file_key


def upload_image_to_s3_from_url(image_url, s3_file_key, bucket_name='aigface'):
    try:
        # Step 1: Stream the image from the URL
        response = requests.get(image_url, stream=True)
        response.raise_for_status()  # Ensure the request was successful

        # Step 2: Upload the image content directly to S3
        s3.upload_fileobj(response.raw, bucket_name, s3_file_key)
        return f"https://{bucket_name}.s3.amazonaws.com/{s3_file_key}"
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image from {image_url}: {e}")
