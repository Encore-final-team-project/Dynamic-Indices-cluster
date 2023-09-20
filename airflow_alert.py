from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.email_operator import EmailOperator
import shutil

def check_disk_space():
    total, used, free = shutil.disk_usage("/")
    used_percent = (used / total) * 100
    return used_percent

def decide_which_task():
    if check_disk_space() > 80:
        return 'send_email'
    return 'do_nothing'

default_args = {
    'owner': 'outsider',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 19),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    dag_id = 'disk_space_monitor',
    default_args=default_args,
    description='A simple DAG to monitor disk space',
    schedule_interval=timedelta(minutes=60),  # Adjust this as needed
    catchup=False,
)

decision = BranchPythonOperator(
    task_id='check_disk_space',
    python_callable=decide_which_task,
    provide_context=True,
    dag=dag,
    op_args=[],
    op_kwargs={},
)

send_email = EmailOperator(
    task_id='send_email',
    to='fearfuloutsider@gmail.com',
    subject='Disk Space Alert',
    html_content='<h3>Disk space exceeded 80%!</h3>',
    dag=dag,
)
do_nothing = PythonOperator(
    task_id='do_nothing',
    python_callable=lambda: 'do_nothing',
    dag=dag,
)
decision >> [send_email, do_nothing]
