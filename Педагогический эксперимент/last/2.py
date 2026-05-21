import boto3
from botocore.client import Config

ACCESS_KEY = "ID_КЛЮЧА"
SECRET_KEY = "СЕКРЕТНЫЙ_КЛЮЧ"

s3_client = boto3.client(
    's3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    config=Config(signature_version='s3v4')
)

with open('image.png', 'rb') as f:
    s3_client.upload_fileobj(f, 'my-bucket', 'image.png')

print("Готово!")