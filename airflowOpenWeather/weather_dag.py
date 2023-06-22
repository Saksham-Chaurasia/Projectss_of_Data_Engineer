from airflow import DAG
import json
from datetime import datetime, timedelta 
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import pandas as pd
from transforming_data import transform_data


default_args = {'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2023,6,22),
        'email':['saksham84a@gmail.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=2)
        }

with DAG(dag_id='weather_dag',
        default_args=default_args,
        description='weather_api',
        # start_date=datetime(),
        schedule_interval='@daily',
        catchup=False,
        # tags=['']
) as dag:
    
    weather_api_connect = HttpSensor(
        task_id='weather_api_connect',
        http_conn_id='weathermap_api',
        endpoint='data/2.5/weather?q=hyderabad,IN&appid=1aefcb9f02571123f927fa4cfe7e36e6'
    )

    extract_weather_data=SimpleHttpOperator(
        task_id='extract_weather_data',
        http_conn_id='weathermap_api',
        endpoint='data/2.5/weather?q=hyderabad,IN&appid=1aefcb9f02571123f927fa4cfe7e36e6',
        method='GET',
        response_filter=lambda r:json.loads(r.text),
        log_response=True
    )

    transform_weather_data=PythonOperator(
        task_id="transform_weather_data",
        python_callable=transform_data
    )


    weather_api_connect >> extract_weather_data 
    extract_weather_data >> transform_weather_data

    