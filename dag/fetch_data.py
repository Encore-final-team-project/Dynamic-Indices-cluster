from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries

def fetch_apple_price():
    apple = yf.Ticker("AAPL")
    data = apple.history(period="1d")
    # 여기서 DB에 데이터를 저장하는 코드를 작성하시면 됩니다.

def fetch_economic_data():
    ts = TimeSeries(key='QA7AWI9EFI267BNJ', output_format='pandas')
    data, meta_data = ts.get_intraday(symbol='AAPL', interval='1h', outputsize='full')
    # 여기서 DB에 데이터를 저장하는 코드를 작성하시면 됩니다.

default_args = {
    'owner': 'me',
    'start_date': datetime(2023, 8, 21),
}

dag = DAG(
    'apple_data_fetcher',
    default_args=default_args,
    description='애플 주가 정보와 경제지표를 매시간 가져오기',
    schedule_interval='@hourly',
)

fetch_price_task = PythonOperator(
    task_id='fetch_apple_price',
    python_callable=fetch_apple_price,
    dag=dag,
)

fetch_economic_task = PythonOperator(
    task_id='fetch_economic_data',
    python_callable=fetch_economic_data,
    dag=dag,
)

fetch_price_task >> fetch_economic_task
