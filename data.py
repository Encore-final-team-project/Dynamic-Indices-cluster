# yfinance를 이용하여 제무제표 및 실시간 주가데이터를 가져옵니다.

import yfinance as yf

# 원하는 회사의 ticker를 입력합니다.
ticker = "AAPL" # 예시로 Apple의 ticker를 사용했습니다.

# Ticker 객체를 생성합니다.
stock = yf.Ticker(ticker)

# 재무제표를 불러옵니다.
balance_sheet = stock.balance_sheet
income_statement = stock.financials
cash_flow_statement = stock.cashflow



# 최근 1일 동안의 주가 데이터를 가져옵니다.
historical_data = stock.history(period="1d", interval="1m") # '1m'은 1분 간격의 데이터를 의미합니다.


# 결과를 출력합니다.
print(balance_sheet)
print(income_statement)
print(cash_flow_statement)
print(historical_data)

