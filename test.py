import requests

API_URL = "https://www.alphavantage.co/query"
API_KEY = "QA7AWI9EFI267BNJ"  # 여기에 실제 API 키를 입력하세요

# 경제 지표 관련 파라미터 설정 (예시로 MACD 지표를 사용)
parameters = {
    "function": "TIME_SERIES_INTRADAY",  # 이 값을 해당 경제 지표에 알맞게 변경하세요
    "symbol": "MSFT",  # 원하는 주식의 심볼을 입력하세요
    "interval": "5min",  
    "apikey": API_KEY
}

response = requests.get(API_URL, params=parameters)
data = response.json()

print(data)
