import yfinance as yf
import pandas as pd

# NASDAQ 상장 회사 목록 가져오기
nasdaq_listed_companies = pd.read_csv('http://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt', sep='|')
symbols = nasdaq_listed_companies['Symbol'].dropna().tolist()

# 테스트를 위해 처음 10개의 회사만 선택
symbols = symbols

# 모든 회사의 재무제표를 저장할 빈 DataFrame 생성
all_balance_sheets = pd.DataFrame()

for symbol in symbols:
    try:
        ticker = yf.Ticker(symbol)
        balance_sheet = ticker.balance_sheet

        # 칼럼 이름을 년도만으로 변경
        balance_sheet.columns = [str(col).split('-')[0] for col in balance_sheet.columns]

        # 데이터프레임 합치기 전에 'Company' 칼럼 추가
        balance_sheet['Company'] = symbol

        # 재무제표를 전체 데이터프레임에 추가
        all_balance_sheets = pd.concat([all_balance_sheets, balance_sheet], sort=False)
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        continue

# 'Company' 칼럼을 맨 마지막으로 옮김
company_col = all_balance_sheets.pop('Company')
all_balance_sheets['Company'] = company_col

# 칼럼을 년도 순으로 정렬하고, 'Company' 칼럼은 마지막에 위치
all_balance_sheets = all_balance_sheets.sort_index(axis=1)

# 결과 저장
all_balance_sheets.to_csv("test_nasdaq_balance_sheets_yfinance.csv")


