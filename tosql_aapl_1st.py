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
def fetch_balance_sheet(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "BALANCE_SHEET",
        "symbol": symbol,
        "apikey": "QA7AWI9EFI267BNJ"
    }
    headers = {"accept": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data

# 이 부분을 추가하여 DB에서 symbol 이름들을 가져옵니다.
def get_symbol_names():
    # 적절한 쿼리를 사용하여 symbol 이름들을 가져오는 코드를 작성하세요.
    # 예시: SELECT symbol_name FROM symbol_table;
    curs =
    symbol_names = []  # 심볼 이름들을 담을 리스트
    # 여기에 적절한 DB 쿼리를 실행하여 symbol_names 리스트를 채우는 코드를 작성하세요.
    return symbol_names

def store_data(data):
    # Extract balance sheet data
    balance_sheet = data.get("annualReports", [])
    
    if not balance_sheet:
        print("No balance sheet data available.")
        return
    
    # Create a DataFrame
    df = pd.DataFrame(balance_sheet)
    
    # Store the data in the MySQL database
    df.to_sql(name="aapl_balance_sheet", con=engine, if_exists='replace', index=False)

def main():
    balance_sheet_data = fetch_balance_sheet()
    store_data(balance_sheet_data)

if __name__ == "__main__":
    main()