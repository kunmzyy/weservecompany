from configparser import ConfigParser
import pandas as pd
from sql_statements.transform import transform_tables 
from utils.helper import s3_path, bucket_name, access_key, secret_key


def extract_received_calls_df():
    df = transform_tables()
    df = df[['id', 'call_id', 'caller_id', 'recieving_agent_id', 'complaint_topic', 'assigned_agent_id', 'complaint_status',
                'call_duration_in_seconds', 'call_type', 'call_ended_by_agent']]
    file = 'all_calls'
    df.to_csv(s3_path.format(bucket_name, file), index=False, storage_options={
            'key': access_key,
            'secret': secret_key
        }
    )

# Extracting all recieved calls - all inbound calls


def extract_recieved_calls_df():
    df = transform_tables()
    df = df[['call_type'] == 'Inbound'][['call_id', 'caller_id', 'call_type', 'complaint_topic',
                                                       'call_duration_in_seconds', 'recieving_agent_id', 'assigned_agent_id']]
    df = df.reset_index(drop=True)
    file = 'recieve'
    df.to_csv(s3_path.format(bucket_name, file), index=False, storage_options={
        'key': access_key,
        'secret': secret_key
    })


def extract_resolved_calls_df():
    df = transform_tables()
    df = df[(['complaint_status'] == 'resolved') | (df['complaint_status'] == 'closed')][[
        'call_id', 'caller_id', 'recieving_agent_id', 'complaint_topic', 'complaint_status', 'assigned_agent_id', 'resolution_duration_in_hours']]

    file = 'resolve'
    df.to_csv(s3_path.format(bucket_name, file), index=False, storage_options={
        'key': access_key,
        'secret': secret_key
    })





def extract_agents_df():
    df = transform_tables()
    agent_df = df[['recieving_agent_id', 'call_id', 'call_type',
                   'call_duration_in_seconds', 'agents_grade_level']].sort_values('recieving_agent_id')
    file = 'agents'
    agent_df.to_csv(s3_path.format(bucket_name, file), index=False, storage_options={
        'key': access_key,
        'secret': secret_key
    })


def extract_complaint_df():
    # Read the created function from transformation.py
    df = transform_tables()
    df = df[['id', 'call_id', 'complaint_topic', 'complaint_status']]
    df = df.reset_index(drop=True)
    file = 'complaints'
    df.to_csv(s3_path.format(bucket_name, file), index=False, storage_options={
        'key': access_key,
        'secret': secret_key
    })

def extract_assigned_df():
    df = transform_tables()
    df = df.loc[df['assigned_calls_to_agent_id'].notnull()][['call_id', 'caller_id',
                                                             'assigned_calls_to_agent_id', 'complaint_status']]
    df['assigned_calls_to_agent_id'] = df['assigned_calls_to_agent_id'].astype(
        int)
    file = 'assigned_calls'
    df.to_csv(s3_path.format(bucket_name, file), index=False, storage_options={
        'key': access_key,
        'secret': secret_key
    })

extract_jobs = [extract_agents_df, extract_received_calls_df,
                extract_recieved_calls_df, extract_resolved_calls_df, extract_complaint_df]

