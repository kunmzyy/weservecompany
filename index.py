
import psycopg2
import pandas as pd
import boto3
import configparser
from extraction import extract_recieved_calls_df
from sqlalchemy import create_engine
from utils.helper import bucket_name

from utils.constants import tables
from utils.helper import connect_to_dwh
from sql_statements.create import raw_data
from sql_statements.transform import staging_data
from utils.constants import tables
from sql_statements.insert import insert_into_transform
from utils.helper import (bucket_name, connect_to_dwh,
                      create_s3_bucket)
from extraction import extract_jobs
from utils.constants import tables


config= configparser.ConfigParser()
config.read('.env')

access_key = 'AKIA2JVK4EED4UIH35QD'
secret_key = '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'


region=config['AWS']['region']
bucket_name=config['AWS']['bucket_name']
access_key=config['AWS']['access_key']
secret_key=config['AWS']['secret_key']
role=config['AWS']['role']





dwh_host=config['DWH']['host']
dwh_user=config['DWH']['user']
dwh_password=config['DWH']['password']
dwh_database=config['DWH']['database']

Raw_data = config['DWH']['raw_data']
staging_data = config['DWH']['staging_data']









def extract_all_jobs():
    for job in extract_jobs:
        job()


# Raw schema and dev schema in data warehouse

def raw_data():
    conn = connect_to_dwh()
    cursor = conn.cursor()
    print('Create raw schema')
    cursor.execute(raw_data.format(raw_data))
    conn.commit()
    cursor.close()




def staging_data():
    conn = connect_to_dwh()
    cursor = conn.cursor()
    print(create_staging_data.__name__)
    cursor.execute(raw_call_schema.format(staging_data))
    conn.commit()
    cursor.close()



def create_raw_tables():
    for query in raw_data:
        conn = connect_to_dwh()
        cursor = conn.cursor()
        print(f"{query[:35]}")
        cursor.execute(query.format(raw_data))
        conn.commit()
        print('All tables created')
    cursor.close()




def create_trans_tables():
    for query in transform_tables:
        conn = connect_to_dwh()
        cursor = conn.cursor()
        print(f"{query[:45]}")
        cursor.execute(query.format(staging_data))
        conn.commit()
        print('All transform tables created')
    cursor.close()



def copy_from_s3_dwh():
    try:
        dwh_conn = connect_to_dwh()
        cursor = dwh_conn.cursor()
        for table in transform_tables:
            print(f"Copying {table} from s3 to DWH")
            table_copy_query = f"""
            copy {raw_data}.{table}
            from '{s3_path.format(bucket_name, table)}'
            iam_role '{role}'
            delimiter ','
            ignoreheader 1;
        """
            cursor.execute(table_copy_query)
            dwh_conn.commit()
        cursor.close()
        dwh_conn.close()
    except Exception as e:
        print(e)




def insert_into_trans_tables():
    for query in insert_into_transform:
        conn = connect_to_dwh()
        cursor = conn.cursor()
        print(f"{query[:20]}")
        cursor.execute(query.format(staging_data))
        conn.commit()
    print('All transform tables inserted')
    cursor.close()


def running_all_functions_jobs():
    create_s3_bucket()
    extract_all_jobs()
    raw_data()
    staging_data()
    create_raw_tables()
    create_trans_tables()
    copy_from_s3_dwh()
    insert_into_trans_tables()








