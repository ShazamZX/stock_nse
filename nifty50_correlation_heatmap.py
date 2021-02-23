# -*- coding: utf-8 -*-
"""NIFTY50 Correlation Heatmap

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/ShazamZX/stock_nse/blob/main/NIFTY50_Correlation_Heatmap.ipynb
"""

import pandas as pd
import pandas_datareader as web
import pickle
from google.colab import files
import datetime as dt
from dateutil.relativedelta import relativedelta
import seaborn as sms
import matplotlib.pyplot as plt

files.upload()

#loading the symbols into dataframe and getting timespan of 1 year
symbol = []
with open("Nifty50.pickle",'rb') as f:
  symbol = pickle.load(f)
end = dt.datetime.date(dt.datetime.now())
start = end + relativedelta(years = -1)

#getting the Adjusted Close for each Company
def get_adjclose(ticker):
  df = web.DataReader(ticker,'yahoo',start, end)
  df.reset_index(inplace = True)
  df.set_index('Date',inplace = True)
  df.rename(columns = {'Adj Close': ticker}, inplace = True)
  return df[ticker].to_frame()

#Creating the correlation DataFrame
def correlation(ticker):
  main = pd.DataFrame()
  for i in ticker:
    temp = get_adjclose(i)
    if main.empty:
      main = temp
    else:
      main = main.join(temp, how = 'outer')
  df_corr = main.corr() 
  return df_corr

corr_df = correlation(symbol)
corr_df.to_csv('NIFTYcorr.csv')

files.download('NIFTYcorr.csv')

#Plotting the heatmap
ax = sms.heatmap(corr_df, center = 0, cmap = 'RdYlGn', annot = True , linewidth = 0.5)