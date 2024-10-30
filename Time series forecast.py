#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd


# In[ ]:


# Loading the stocks data
stocks_data = pd.read_csv(r"C:\Users\daksh\Desktop\Project\stocks.csv")


# In[ ]:


stocks_data.head()


# In[ ]:


# Changing data type of date column to date time for analysis
stocks_data['Date'] = pd.to_datetime(stocks_data['Date'])


# In[ ]:


# Calculating number of missing vaules in each column
missing_values = stocks_data.isnull().sum()
print(missing_values)


# In[ ]:


# Checking for number of unique stocks in teh dataset along with there count
unique_stocks = stocks_data['Ticker'].value_counts()
print(unique_stocks)


# In[ ]:


# Calculating the time frame for the dataset
time_range = stocks_data['Date'].min() , stocks_data['Date'].max()
print(time_range)


# In[ ]:


# visualizing the closing prices trends of each stocks

import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize = (14,8))

for ticker in unique_stocks.index:
    subset = stocks_data[stocks_data['Ticker'] == ticker]
    plt.plot(subset['Date'], subset['Close'], label = ticker)
    
ax.set_title('Closing Price Trends for AAPL, MSFT, NFLX, GOOG')
ax.set_xlabel('Date')
ax.set_ylabel('Closing Price(USD)')
ax.legend()

plt.show()


# In[ ]:


from statsmodels.tsa.stattools import adfuller

# function to perform Augmented Dickey-Fuller test
def adf_test(series, title=''):
    print(f'ADF Test on "{title}"')
    result = adfuller(series, autolag='AIC')  # ADF test
    labels = ['ADF Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used']
    out = pd.Series(result[0:4], index=labels)

    for key, value in result[4].items():
        out[f'Critical Value ({key})'] = value
    print(out.to_string()) 
    print('\n')

# perform ADF test on the 'Close' price of each stock
for ticker in unique_stocks.index:
    series = stocks_data[stocks_data['Ticker'] == ticker]['Close']
    adf_test(series, title=ticker)


# In[ ]:


# differencing the 'Close' price of each stock to make the series stationary
stocks_data['Diff_Close'] = stocks_data.groupby('Ticker')['Close'].transform(lambda x: x.diff())

for ticker in unique_stocks.index:
    series = stocks_data[stocks_data['Ticker'] == ticker]['Diff_Close'].dropna()
    adf_test(series, title=f"{ticker} - Differenced")


# In[ ]:


# training the data model
from statsmodels.tsa.vector_ar.var_model import VAR

var_data = stocks_data.pivot(index='Date',columns='Ticker', values='Diff_Close').dropna()

model = VAR (var_data)

model_fitted = model.fit(ic= 'aic')

forecast_steps = 5

forecasted_values = model_fitted.forecast(var_data.values[-model_fitted.k_ar:], steps=forecast_steps)

forecasted_df = pd.DataFrame(forecasted_values, index=pd.date_range(start=var_data.index[-1] + pd.Timedelta(days=1), periods=forecast_steps, freq='D'), columns=var_data.columns)

for column in forecasted_df.columns:
    forecasted_df[column] = (stocks_data.groupby('Ticker')['Close'].last()[column] + forecasted_df[column].cumsum())

print(forecasted_df)


# In[ ]:


fig, ax = plt.subplots(figsize=(14, 8))

# plot historical closing prices for each stock
for ticker in unique_stocks.index:
    historical_data = stocks_data[stocks_data['Ticker'] == ticker]
    ax.plot(historical_data['Date'], historical_data['Close'], label=ticker)

# plot the forecasted closing prices
for column in forecasted_df.columns:
    ax.plot(forecasted_df.index, forecasted_df[column], label=f'{column} Forecast', linestyle='--')

ax.set_title('Historical and Forecasted Closing Prices')
ax.set_xlabel('Date')
ax.set_ylabel('Closing Price (USD)')
ax.legend()

plt.xticks(rotation=45)
plt.show()


# In[ ]:



