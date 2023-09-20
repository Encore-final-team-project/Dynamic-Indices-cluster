import yfinance as yf
import pandas as pd
import pymysql
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from config import Config, Lake
from SymbolList import Symbols

db_type = Config['db_type']
username = Config['username']
password = Config['password']
host = Config['host']
port = Config['port']
database1 = Lake['database1']
database2 = Lake['database2']
database3 = Lake['database3']

symbols = Symbols()

# 각 회사의 주가 정보 가져오기
def fetch_stock_data():
    end_date = datetime.today()
    start_date = end_date - timedelta(days=1)

    all_data = []

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

    final_data = pd.concat(all_data)
    return final_data

# 데이터베이스에 데이터 저장
def save_to_db():
    engine = create_engine(f'{db_type}://{username}:{password}@{host}:{port}/{database3}')
    data = fetch_stock_data()
    data.reset_index(inplace=True)
    data.to_sql('stock_data', engine, if_exists='append', index=False)

def main():
    save_to_db()

if __name__ == "__main__":
    main()

