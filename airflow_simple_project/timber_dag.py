from airflow import DAG
import json
from datetime import datetime, timedelta
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.sensors.time_sensor import TimeSensor
from airflow.operators.email_operator import EmailOperator
from timberdef import spark_code
from airflow.operators.spark_submit_operator import SparkSubmitOperator

# from pyspark.sql import SparkSession
# from pyspark.sql.functions import format_number
# from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
import pandas as pd

default_args = {'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2023,5,4),
        'email':['saksham84a@gmail.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=2)
        }

with DAG('timberland_airflow',
        default_args=default_args,
        description='timberland airflow project with spark',
        schedule_interval='@daily',
        catchup=False
        # start_date=days_ago(2),
        # tags=['example'],
) as dag:
    
    task1 = DummyOperator(task_id='start_task')

    spark_task = PythonOperator(
        task_id='spark_task',
        python_callable=spark_code
    )

    end_task = DummyOperator(
        task_id = "end_task"
    )

    email_task = EmailOperator(
        task_id="email_task",
        to=['saksham84a@gmail.com'],
        subject="Airflow successfull!",
        html_content="<i>Message from Airflow -->the output file is generated t</i>"
        # cc=['admin@example.com'],
        # bcc=['audit@example.com'],
        # files=['file1.txt'],
        # mime_subtype: str = 'mixed',
        # mime_charset: str = 'utf-8',
    
    )



task1 >> spark_task >> end_task >> email_task
