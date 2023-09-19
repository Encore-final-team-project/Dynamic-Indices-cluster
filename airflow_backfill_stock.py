from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from backfill_stock import fetch_and_store_data

default_args = {
    'owner': 'outsider',
    'depends_on_past': False,
    'email': ['fearfuloutsider@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id = 'sp500_backfill',
    default_args = default_args,
    description = 'Fetch S&P 500 stock data and store in DB',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 8, 15),
    end_date=datetime(2023, 12, 31),
    catchup=True
)
t1 = PythonOperator(
    task_id='fetch_and_store_MissingData',
    python_callable=fetch_and_store_data,
    provide_context=True,
    dag=dag,
)
if __name__ == "__main__":
    dag.cli()