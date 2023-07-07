from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta 
from sparkawscode import spark_code

dag_owner = 'airflow_aws'

bucket_name ='timberbucket'
file_key ='timberland_stock.csv'



default_args = {'owner': dag_owner,
        'depends_on_past': False,
        'start_date': datetime(2023,5,4),
        'email':['saksham84a@gmail.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
        }



with DAG(dag_id='airflow_aws_connect',
        default_args=default_args,
        description='airflow aws implementation',
        schedule_interval='@daily',
        catchup=False,
        # tags=['']
)as dag:
    
    start = DummyOperator(task_id='start')


    # task2 = PythonOperator(
    #     task_id='read_csv_task',
    #     python_callable=read_csv_from_s3,
    #     op_kwargs={'bucket_name':'timberbucket','file_key':'timberland_stock.csv'}
    # )

    task2 = PythonOperator(
        task_id='spark_task',
        python_callable=spark_code,
        op_kwargs={'bucket_name':'timberbucket','file_key':'timberland_stock.csv'}
    )

start >> task2 

    