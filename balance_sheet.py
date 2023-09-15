import yfinance as yf
import pandas as pd
import pymysql
from sqlalchemy import create_engine
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

# finance DB 연결 엔진 (create는 finance에서)
engine = create_engine(f'{db_type}://{username}:{password}@{host}:{port}/{database1}')

symbols = Symbols()

def main():
    # symbol 리스트를 통해 finance DB에 data 적재
    for symbol in symbols:
        data_yf = yf.Ticker(symbol).balance_sheet

        if data_yf is None or data_yf.empty:
            print(f"No data available for symbol: {symbol}. Skipping...")
            continue

        data_df = pd.DataFrame(data_yf)
        bs = data_df.transpose()    # balance sheet (dataframe) 완성

        bs['Symbol'] = symbol     # Symbol 붙여주기

        table_name = f'{symbol}_balance_sheet'

        try:
            # MySQL 테이블이 이미 존재하는 경우 덮어쓰기
            bs.to_sql(name=table_name, con=engine, if_exists='append', index=True)
            print(symbol, ' complete!')
        except Exception as e:
            print(f"Error for symbol {symbol}: {str(e)}")
            continue  # 오류가 발생한 경우 다음 symbol로 넘어가기

if __name__ == "__main__":
    main()
