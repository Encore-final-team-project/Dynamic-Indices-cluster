import yfinance as yf
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from config import Config, Lake
from SymbolList import Symbols

# DB config 정보
db_type = Config['db_type']
username = Config['username']
password = Config['password']
host = Config['host']
port = Config['port']
database1 = Lake['database1']
database2 = Lake['database2']
database3 = Lake['database3']

def main():
    # DB create_engine
    engine = create_engine(f'{db_type}://{username}:{password}@{host}:{port}/{database1}')

    symbols = Symbols()

    # finance DB
    for symbol in symbols:
        data_yf = yf.Ticker(symbol).cashflow

        if data_yf is None or data_yf.empty:
            print(f"No data available for symbol: {symbol}. Skipping...")
            continue

        data_df = pd.DataFrame(data_yf) # DataFrame을 ㅓ작게 해서 읽어보기 (***)
        # pandas Modin dask
        cf = data_df.transpose()    # cash flow (dataframe) 완성

        cf['Symbol'] = symbol     # Symbol 붙여주기

        table_name = f'{symbol}_cash_flow'

        # MySQL 테이블이 이미 존재하는 경우 덮어쓰기
        cf.to_sql(name=table_name, con=engine, if_exists='append', index=True)
        print(symbol, ' complete!')

if __name__ == "__main__":
    main()
