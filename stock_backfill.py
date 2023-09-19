from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'outsider',
    'depends_on_past': False,
    'email': ['fearfuloutsider@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
def fetch_and_store_data(execution_date):
    # 주어진 execution_date 기준으로 시작/종료 날짜 계산
    end_date = execution_date
    start_date = end_date - timedelta(days=30)

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
    op_args=[{{ ds }}],  # ds는 Airflow의 내장 Jinja template 변수로 execution_date를 문자열로 반환합니다.
    dag=dag,
)
if __name__ == "__main__":
    dag.cli()