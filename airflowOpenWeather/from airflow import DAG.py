from airflow import DAG    
from datetime import timedelta,datetime  
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator 


def first_program():
    print("hello world")


default_args = {
    'owner':'first_program',
    'depends_on_past':False,
    'start_date':datetime(2023,5,22),
    'email':['saksham84a@gmail.com'],
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':2,
    'retry_delay':timedelta(minutes=2)

}

with DAG(
        dag_id = 'practice_dag',
        default_args=default_args,
        description='printing_dag',
        schedule_interval=timedelta(days=1),
        catchup=False,
        # start_date=days_ago(2),
        # tags=['example'],
) as dag:

# creting first task
    task1 = DummyOperator(
        task_id="start_task"
        
    )
    task2 = PythonOperator(
        task_id="first_task",
        python_callable = first_program
        
    )

    task3 = DummyOperator(
        task_id = 'end_task'
    )


    task1 >> task2 >> task3
