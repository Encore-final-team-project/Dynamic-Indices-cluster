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

def testStock():
    for tt in ran:
        company_indexing = company[tt]
        period = yf.download(company_indexing, interval='1m', period='1d')
        date = period.index
        date= date.to_frame()
        openp = period['Open']
        highp = period['High']
        lowp = period['Low']
        closep = period['Close']
        volumep = period['Volume']

        adjclosep = period['Adj Volume']
        mergep = pd.concat([date, volumep, highp, lowp, openp, closep, adjclosep], axis=1)#, divip, splitsp)
    return mergep




    

