import pandas as pd
from pandas_datareader import data as pdr
from datetime import datetime, timedelta
import yfinance as yf
import requests

yf.pdr_override()


#data = pdr.get_data_yahoo("^KS11", start="2020-01-01", end="2021-01-01")

#print(data)

cdf = pd.read_csv('ciklist_nasdaq.csv')

company = cdf['ticker']

ran = company.index
sorted_stock = pd.DataFrame()

for tt in ran:
    company_indexing = company[tt]
    ##ticker = yf.Ticker(company_indexing)
    period = yf.download(company_indexing, interval='1m', period='1d')
    #print(period)
    date = period.index
    date= date.to_frame()
    openp = period['Open']
    highp = period['High']
    lowp = period['Low']
    closep = period['Close']
    volumep = period['Volume']
    #divip = period['Dividends']
    #splitsp = period['Stock Splits']
    mergep = pd.concat([date, volumep, highp, lowp, openp, closep], axis=1)#, divip, splitsp)
    print(mergep)
    ###print(period)
    #print(company_indexing)
    ##stock_list = ticker.history()
    #print(stock_list)
    ##company_name = company[tt]
    ##open = stock_list['Open']
    ##high = stock_list['High']
    ##low = stock_list['Low']
    ##close = stock_list['Close']
    ##volume = stock_list['Volume']
    ##dividends = stock_list['Dividends']
    ##splits = stock_list['Stock Splits']
    #print(stock_list.index)
    



    

