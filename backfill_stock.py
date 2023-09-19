import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from config import Config, Lake

db_type = Config['db_type']
username = Config['username']
password = Config['password']
host = Config['host']
port = Config['port']
database1 = Lake['database1']
database2 = Lake['database2']
database3 = Lake['database3']

def fetch_and_store_data(**kwargs):
    execution_date = kwargs['execution_date']  # execution_date 가져오기
    end_date = execution_date.date()
    start_date = end_date - timedelta(days=30)

    # 1. Wikipedia에서 S&P 500 회사 목록 가져오기
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]
    symbols = df['Symbol'].tolist()

    all_data = []

    # 2. 각 회사의 1달간 주가 정보 가져오기
    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            hist = stock.history(start=start_date, end=end_date)

            # 등락률 계산
            hist['Change'] = hist['Close'].pct_change() * 100
            hist['Symbol'] = symbol
            all_data.append(hist)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    # 모든 데이터를 하나의 데이터프레임으로 합치기
    final_data = pd.concat(all_data)

    # 3. 데이터베이스에 데이터 저장
    engine = create_engine(f'{db_type}://{username}:{password}@{host}:{port}/{database3}')
    final_data.reset_index(inplace=True)  # Date를 칼럼으로 변경
    final_data.to_sql('stock_data', engine, if_exists='append', index=False)