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

# SELECT function
def fetching(symbol):   # Symbol 값을 입력받아서 필요한 행만 SELECT
    # DB 연결
    conn = pymysql.connect(host=host, user=username, password=password, database=database1, port=int(port))
    try:
        with conn.cursor() as curs:  # 커서 생성
            string = f'''
              SELECT
                Symbol,
                `index` as indexDate,
                `Total Revenue` as `Revenue`,
                `Operating expense` as `Operating expense`,
                `Net Income` as `Net Income`,
                (`Gross Profit`/`Total Revenue`)*100 as `Net profit margin`,
                `Normalized EBITDA` as `EBITDA`
              FROM {symbol}_income_statement    ;
                      '''
            sql = string
            curs.execute(sql)
            result = curs.fetchall()
    finally:
        conn.close()  # 연결 닫기
    return result

# INSERT function
def store_data(symbol, objdata):
    conn = pymysql.connect(host=host, user=username, password=password, database=database2, port=int(port))
    try:
        with conn.cursor() as curs:  # 커서 생성
            # 데이터를 삽입하는 쿼리를 작성하고 데이터 삽입
            for row in objdata:
              # 각 행(row)을 SQL INSERT 문으로 변환
              sql = f"INSERT INTO fs (Symbol,indexDate,`Revenue`,`Operating expense`,`Net Income`,`Net profit margin`,`EBITDA`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
              curs.execute(sql, row)
            conn.commit()  # 변경사항 커밋
            print(symbol,' Insert Done!')
    finally:
        conn.close()

# DELETE function
def delete_data():
    conn = pymysql.connect(host=host, user=username, password=password, database=database2, port=int(port))
    try:
        with conn.cursor() as curs:  # 커서 생성
            sql = 'DELETE FROM fs'
            curs.execute(sql)
            conn.commit()  # 변경사항 커밋
            print('fs table Deleted.')
    finally:
        conn.close()

# Insert 하기 전, 기존 데이터는 Delete
delete_data()

# Operate
for symbol in symbols:
    try:
        store_data(symbol, fetching(symbol))
    except Exception as e:
        # missing_symbol.append(symbol)
        print(f"Error for symbol {symbol}: {str(e)}")
        continue

