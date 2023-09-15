import pendulum
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
# from airflow.operators.python_operator import PythonOperator

local_tz = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'outsider',
    'depends_on_past': True,
    'start_date': datetime(year=2023, month=9, day=15, hour=0, minute=0, tzinfo=local_tz),
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    dag_id = 'outsider_airflow_finance',
    description = 'outsider airflow pipeline',
    tags = ['spark', 'outsider'],
    max_active_runs = 1,
    concurrency = 10,
    schedule_interval = None,       # 1년에 한 번씩 실행하기
    # user_defined_macros={'local_dt': lambda execution_date: execution_date.in_timezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")},
    catchup=False,
    default_args = default_args
)

# Dag 1
BS_dag1 = BashOperator(
    task_id='Balance_Sheet_yf_to_db',
    bash_command="""
        echo "python3 balance_sheet.py"
        """,
    dag=dag
)

CF_dag1 = BashOperator(
    task_id='Cash_Flow_yf_to_db',
    bash_command="""
        echo "python3 cash_flow.py"
        """,
    dag=dag
)

IS_dag1 = BashOperator(
    task_id='Income_Statement_yf_to_db',
    bash_command="""
        echo "python3 income_statement.py"
        """,
    dag=dag
)

# Dag 2
BS_dag2 = BashOperator(
    task_id='Balance_Sheet_db_edit',
    bash_command="""
        echo "python3 bs.py"
        """,
    dag=dag
)

CF_dag2 = BashOperator(
    task_id='Cash_Flow_db_edit',
    bash_command="""
        echo "python3 cf.py"
        """,
    dag=dag
)

IS_dag2 = BashOperator(
    task_id='Income_Statement_db_edit',
    bash_command="""
        echo "python3 fs.py"
        """,
    dag=dag
)

# DAG 실행
if __name__ == "__main__":
    dag.cli()

# SPARK
# spark_step_1_task_cmd = "echo `date`"
# spark_step_1_task = gen_bash_task("spark_step_1", spark_step_1_task_cmd, dag) # marin_airflow_util - ("id", command, dag_name)

# DummyOperator
start_task = DummyOperator(task_id="start", dag=dag)
end_task = DummyOperator(task_id="end", dag=dag)
mid_task = DummyOperator(task_id="mid", dag=dag)

# WF
start_task >> BS_dag1 >> CF_dag1 >> IS_dag1 >> mid_task
mid_task >> BS_dag2 >> CF_dag2 >> IS_dag2 >> end_task
