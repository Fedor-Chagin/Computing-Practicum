import boto3
from botocore.client import Config

ACCESS_KEY = "ИДЕНТИФИКАТОР_КЛЮЧА"
SECRET_KEY = "СЕКРЕТНЫЙ_КЛЮЧ"

def create_yandex_s3_client():
    """
    Создаёт и возвращает S3-клиент для Yandex Object Storage
    """
    session = boto3.session.Session()
    
    client = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(
            signature_version='s3v4',
            region_name='ru-central1'
        )
    )
    
    return client

# Пример использования
if __name__ == "__main__":
    s3_client = create_yandex_s3_client()
    
    # Проверка подключения: список бакетов
    try:
        buckets = s3_client.list_buckets()
        print("Доступные бакеты:")
        for bucket in buckets.get('Buckets', []):
            print(f"  - {bucket['Name']}")
    except Exception as e:
        print(f"Ошибка подключения: {e}")