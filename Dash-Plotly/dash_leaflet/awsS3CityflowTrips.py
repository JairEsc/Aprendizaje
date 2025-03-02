import boto3
from io import TextIOWrapper
from gzip import GzipFile
import csv
import pandas as pd
import os

def getListRoutesFiles():
# Acceder a las variables de entorno
    access_key = os.getenv('AWS_ACCES_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    s3 = boto3.client('s3', aws_access_key_id=access_key,
            aws_secret_access_key=secret_key)
    bucket_name = 'citydata.hidalgo'

    response = s3.list_objects_v2(Bucket=bucket_name)
    list=[]
    if 'Contents' in response:
        for obj in response['Contents']:
            if 'routes' not in obj['Key'] and '.csv.gz' in obj['Key']:
                list.append(obj['Key'])
    else:
        print("No objects found in the bucket.")
    return list