import requests
import pandas as pd
from sqlalchemy import create_engine
from time import sleep
from config import Config, Lake

db_type=Config['db_type']
username=Config['username']
password=Config['password']
host=Config['host']
port=Config['port']
database=Lake['database1']

cnt = 10

# 데이터베이스 연결 엔진 생성
engine = create_engine(f'{db_type}://{username}:{password}@{host}:{port}/{database}')
def fetch_balance_sheet():
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "BALANCE_SHEET",
        "symbol": "AAPL",
        "apikey": "QA7AWI9EFI267BNJ"
    }
    headers = {"accept": "application/json"}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    return data

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