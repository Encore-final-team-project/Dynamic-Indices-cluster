import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
import requests

yf.pdr_override()


#data = pdr.get_data_yahoo("^KS11", start="2020-01-01", end="2021-01-01")

#print(data)

cdf = pd.read_csv('ciklist_nasdaq.csv')

company = cdf['ticker']

ran = company.index

for tt in ran:
    company_indexing = company[tt]
    ticker = yf.Ticker(company_indexing)
    #print(company_indexing)
    stock_list = ticker.history()
    #print(stock_list)
    company_name = company[tt]
    open = stock_list['Open']
    high = stock_list['High']
    low = stock_list['Low']
    close = stock_list['Close']
    volume = stock_list['Volume']
    dividends = stock_list['Dividends']
    splits = stock_list['Stock Splits']
    print(company_name, volume)



