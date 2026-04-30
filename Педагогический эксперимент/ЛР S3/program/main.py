#!/usr/bin/env python
#-*- coding: utf-8 -*-
import boto3
session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net'
)

# Загрузить объекты в бакет

## Из строки
s3.put_object(Bucket='bucket-service-account-1', Key='/Users/fedorcagin/Documents/toggle_test', Body='TEST', StorageClass='STANDARD')

# ## Из файла
# s3.upload_file('this_script.py', 'bucket-service-account-1', 'py_script.py')
# s3.upload_file('this_script.py', 'bucket-service-account-1', 'script/py_script.py')

# # Получить список объектов в бакете
# for key in s3.list_objects(Bucket='bucket-service-account-1')['Contents']:
#     print(key['Key'])

# # Удалить несколько объектов
# forDeletion = [{'Key':'object_name'}, {'Key':'script/py_script.py'}]
# response = s3.delete_objects(Bucket='bucket-service-account-1', Delete={'Objects': forDeletion})

# # Получить объект
# get_object_response = s3.get_object(Bucket='bucket-service-account-1',Key='py_script.py')
# print(get_object_response['Body'].read())