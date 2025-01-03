import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#download TSM data 
def get_tsm_data(start_date = '1997-10-09', end_date = 'None'):
  "Download TSM data from Yahoo Finance"
  tsm = yf.download('TSM', start=start_date, end=end_date)
# Calculate daily returns
  tsm['Returns'] = tsm['Close'].pct_change()

# Basic statistics
  print(tsm['Returns'].describe())

# Plot closing prices
  plt.figure(figsize=(12,6))
  plt.plot(tsm['Close'])
  plt.title('TSM Stock Price')
  plt.xlabel('Date')
  plt.ylabel('Price')
  plt.show()
    
if __name__ == '__main__':
  data = get_tsm_data()
  print(data.head())
