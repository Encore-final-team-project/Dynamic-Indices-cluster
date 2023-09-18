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

def main():
    # MySQL 연결 설정
    engine = create_engine(f'{db_type}://{username}:{password}@{host}:{port}/{database1}')

    symbols = Symbols()

    for symbol in symbols:
        data_yf = yf.Ticker(symbol).financials

        if data_yf is None or data_yf.empty:
            print(f"No data available for symbol: {symbol}. Skipping...")
            continue

        data_df = pd.DataFrame(data_yf)
        fs = data_df.transpose()    # balance sheet (dataframe) 완성

        fs['Symbol'] = symbol     # Symbol 붙여주기

        table_name = f'{symbol}_income_statement'

        # MySQL 테이블이 이미 존재하는 경우 덮어쓰기
        fs.to_sql(name=table_name, con=engine, if_exists='append', index=True)
        print(symbol, ' complete!')

if __name__ == "__main__":
    main()