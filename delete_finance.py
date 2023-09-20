import pymysql
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

def delete_balance_sheet(symbol, conn):
    try:
        with conn.cursor() as curs:  # 커서 생성
            # 데이터를 삭제하는 쿼리를 작성하고 데이터 삭제
            sql = f"DELETE FROM {symbol}_balance_sheet"
            curs.execute(sql)
            conn.commit()  # 변경사항 커밋
    finally:
            print(symbol,' balance sheet Delete Done!')

def delete_cash_flow(symbol, conn):
    try:
        with conn.cursor() as curs:  # 커서 생성
            # 데이터를 삭제하는 쿼리를 작성하고 데이터 삭제
            sql = f"DELETE FROM {symbol}_cash_flow"
            curs.execute(sql)
            conn.commit()  # 변경사항 커밋
    finally:
            print(symbol,' cash flow Delete Done!')

def delete_income_statement(symbol, conn):
    try:
        with conn.cursor() as curs:  # 커서 생성
            # 데이터를 삭제하는 쿼리를 작성하고 데이터 삭제
            sql = f"DELETE FROM {symbol}_income_statement"
            curs.execute(sql)
            conn.commit()  # 변경사항 커밋
    finally:
            print(symbol,' income statement Delete Done!')

# main 은 이곳에 있다
conn = pymysql.connect(host=host, user=username, password=password, database=database1, port=int(port))
for symbol in symbols:
    try:
        delete_balance_sheet(symbol, conn)
        delete_cash_flow(symbol, conn)
        delete_incomee_statement(symbol, conn)
    except Exception as e:
        print(f"Error for symbol {symbol}: {str(e)}")
        continue
conn.close()

