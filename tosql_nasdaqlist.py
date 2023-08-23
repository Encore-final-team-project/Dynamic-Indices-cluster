import requests
import pandas as pd
from sqlalchemy import create_engine
from config import Config, Lake

db_type = Config['db_type']
username = Config['username']
password = Config['password']
host = Config['host']
port = Config['port']
database = Lake['database1']

# 데이터베이스 연결 엔진 생성
engine = create_engine(f'{db_type}://{username}:{password}@{host}:{port}/{database}')

def fetch_nasdaq_data():
    url = "http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
    response = requests.get(url)
    data_lines = response.text.splitlines()
    header = data_lines[0].split('|')
    data = [line.split('|') for line in data_lines[1:]]
    df = pd.DataFrame(data, columns=header)
    return df

def store_data(data_frame):
    # Store the data in the MySQL database
    data_frame.to_sql(name="nasdaq_listed", con=engine, if_exists='replace', index=False)

def main():
    nasdaq_data = fetch_nasdaq_data()
    store_data(nasdaq_data)

if __name__ == "__main__":
    main()
