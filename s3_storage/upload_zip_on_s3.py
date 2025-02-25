import os

import boto3
from botocore.exceptions import ClientError
from s3_storage.get_s3_conn import get_conn

# Создаем сессию и клиент S3
session = boto3.session.Session()

s3 = get_conn()

# Параметры
bucket_name = 'the-lab-bucket'
local_dir = '../output_zip/'
s3_prefix = 'cvat/input/'


# Проверка существования файла в S3
def file_exists_in_s3(bucket, key):
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise


# Загружаем файлы в S3 только если их нет

def upload_files_to_s3(local_dir, bucket_name, s3_prefix):
    for root, _, files in os.walk(local_dir):
        for file in files:
            if file.endswith('.zip'):
                local_path = os.path.join(root, file)
                s3_path = s3_prefix + file

                if file_exists_in_s3(bucket_name, s3_path):
                    print(f"File {file} already exists in s3://{bucket_name}/{s3_path}. Skipping upload.")
                else:
                    s3.upload_file(local_path, bucket_name, s3_path)
                    print(f"Uploaded {file} to s3://{bucket_name}/{s3_path}")


# Загружаем файлы и создаем манифест
upload_files_to_s3(local_dir, bucket_name, s3_prefix)
