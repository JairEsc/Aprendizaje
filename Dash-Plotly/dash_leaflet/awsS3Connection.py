import boto3
from io import TextIOWrapper
from gzip import GzipFile
import csv
import pandas as pd
import os

# Acceder a las variables de entorno
access_key = os.getenv('AWS_ACCES_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
def get_data_given_index(file):
    s3 = boto3.client('s3', aws_access_key_id=access_key,
        aws_secret_access_key=secret_key)
    response = s3.get_object(Bucket='citydata.hidalgo', Key=file)
    gzipped = GzipFile(None, 'rb', fileobj=response['Body'])
    print("---------------------------------")
    #print(gzipped)
    data = TextIOWrapper(gzipped)
    print("---------------------------------")
    #print(data)
    # Initialize counters
    total_lines = 0
    selected_lines = 0

    # Desired columns
    desired_columns = ['overlap_origin_long', 'overlap_origin_lat', 'overlap_destination_long',
                        'overlap_destination_lat', 'trip_speed_mps', 'travel_mode', 'trip_id']

    # Create a CSV reader
    reader = csv.DictReader(data)

    # Create an empty DataFrame with desired columns
    df_final = pd.DataFrame(columns=desired_columns)

    # Process the data
    for row in reader:
        total_lines += 1
        if row['travel_mode'] == 'cycling':
            selected_lines += 1
            selected_data = {col: row[col] for col in desired_columns}
            df_final.loc[total_lines]=[row[col] for col in desired_columns]
        if total_lines ==10000:
            break
    return(df_final)
