import requests
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from time import sleep
from config import Config, Lake

db_type=Config['db_type']
username=Config['username']
password=Config['password']
host=Config['host']
port=Config['port']
database=Lake['database1']

# 데이터베이스 연결 엔진 생성
engine = create_engine(f'{db_type}://{username}:{password}@{host}:{port}/{database}')
def fetch_income_statement(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "INCOME_STATEMENT",
        "symbol": symbol,
        "apikey": "QA7AWI9EFI267BNJ"
    }
    headers = {"accept": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data

# symbol들을 가져오기
def get_symbol_names():
    # DB 연결
    conn = pymysql.connect(host=host, user=username, password=password, database=database, port=int(port))
    try:
        with conn.cursor() as curs:        # 커서 생성
            sql = 'SELECT Symbol FROM symbol_list'
            curs.execute(sql)
            result = curs.fetchall()
            symbol_names = [row[0] for row in result]       # 튜플의 리스트에서 실제 Symbol 값만 추출하여 리스트로 변환
    finally:
        conn.close()        # 연결 닫기
    return symbol_names

def store_data(symbol, data):
    # Extract income_statement data
    income_statement = data.get("annualReports", [])

    if not income_statement:
        print(f"No income_statement data available for symbol: {symbol}")
        return

    # Create a DataFrame
    df = pd.DataFrame(income_statement)

    # Store the data in the MySQL database with the symbol as part of the table name
    table_name = f"{symbol}_income_statement"
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

def main():
    symbol_names = get_symbol_names()  # DB에서 symbol 이름들 가져오기

    for symbol in symbol_names:
        income_statement_data = fetch_income_statement(symbol)
        store_data(symbol, income_statement_data)

if __name__ == "__main__":
    main()
