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
                `Net Income From Continuing Operations` as `Net Income`,
                `Operating Cash Flow` as `Cash from operations`,
                `Investing Cash Flow` as `Cash from investing`,
                `Financing Cash Flow` as `Cash from financing`,
                `Changes In Cash` as `Net change in cash`,
                `Operating Cash Flow`-`Capital Expenditure` as `Free cash flow`
              FROM {symbol}_cash_flow
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
              sql = f"INSERT INTO cf (Symbol,indexDate,`Net Income`,`Cash from operations`,`Cash from investing`,`Cash from financing`,`Net change in cash`,`Free cash flow`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
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
            sql = 'DELETE FROM cf'
            curs.execute(sql)
            conn.commit()  # 변경사항 커밋
            print('cf table Deleted.')
    finally:
        conn.close()

# Insert 하기 전, 기존 데이터는 Delete
delete_data()

def main():
    # Operate
    for symbol in symbols:
        try:
            store_data(symbol, fetching(symbol))
        except Exception as e:
            print(f"Error for symbol {symbol}: {str(e)}")
            continue

if __name__ == "__main__":
    main()

