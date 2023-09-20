import pendulum
import stock
import logging
from airflow import DAG
from datetime import datetime, timedelta
from airflow.utils.log.logging_mixin import LoggingMixin
# from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python_operator import PythonOperator

local_tz = pendulum.timezone("Asia/Seoul")
logger = LoggingMixin().log

default_args = {
    'owner': 'outsider',
    'depends_on_past': True,
    'start_date': datetime(year=2023, month=8, day=15, hour=6, minute=0, tzinfo=local_tz),
    'end_date': datetime(year=2023, month=9, day=20, hour=6, minute=0, tzinfo=local_tz),
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    dag_id = 'outsider_airflow_stock',
    description = 'outsider airflow pipeline - stock',
    tags = ['spark', 'outsider'],
    max_active_runs = 1,
    concurrency = 10,
    schedule_interval = timedelta(days=1),       # 하루에 한 번씩 실행하기
    catchup=True,
    default_args = default_args
)

def run_stock_script():
    stock.main()    # stock.py 파일 내의 main 함수 실행하기

# Dag
STOCK_dag = PythonOperator(
    task_id='Stock_yf_to_db',
    python_callable = run_stock_script,
    dag=dag
)

# DAG 실행
if __name__ == "__main__":
    dag.cli()

# DummyOperator
start_task = DummyOperator(task_id="start", dag=dag)
end_task = DummyOperator(task_id="end", dag=dag)
# mid_task = DummyOperator(task_id="mid", dag=dag)

# WF
start_task >> STOCK_dag >> end_task

logger.setLevel(logging.INFO)
