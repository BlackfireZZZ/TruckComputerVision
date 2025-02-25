import boto3

from private_config import PrivateConfig


def get_conn() -> boto3.client:
    # Создаем сессию S3
    session = boto3.session.Session()

    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=PrivateConfig.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=PrivateConfig.AWS_SECRET_ACCESS_KEY,
    )

    return s3

