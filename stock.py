import yfinance as yf
import pandas as pd
import pymysql
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

def main():
    # yfinance로 정보 수집 및 데이터베이스에 저장
    for symbol in symbols:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            name = info['shortName']
            long_business_summary = info.get('longBusinessSummary', '')

            with engine.connect() as conn:
                conn.execute(company_info.insert().values(symbol=symbol, name=name, longBusinessSummary=long_business_summary))
                conn.commit()  # 트랜잭션 커밋
        except Exception as e:
            print(f"An error occurred while inserting data for {symbol}: {e}")

if __name__ == "__main__":
    main()

