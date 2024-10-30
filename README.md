# Multivariate Time Series Forecasting using Python

This project demonstrates the use of **Multivariate Time Series Forecasting** to predict future stock prices of multiple companies simultaneously, leveraging dependencies between variables. The main focus of this project is on predicting closing prices for Apple (AAPL), Microsoft (MSFT), Netflix (NFLX), and Google (GOOG) using **Vector Auto Regression (VAR)**.

## Project Overview

Unlike univariate time series forecasting, which predicts a single variable (e.g., a single stock), multivariate forecasting captures interdependencies across several variables to make predictions for multiple variables at once. This approach is beneficial when the variables influence each other, allowing more accurate and holistic forecasting.

## Process

### 1. Data Collection and Preparation
- **Data**: Historical stock price data for Apple, Microsoft, Netflix, and Google.
- **Columns**:
  - `Ticker`: Stock symbol
  - `Date`: Trading session date
  - `Open`: Opening price
  - `High`: Highest price
  - `Low`: Lowest price
  - `Close`: Closing price
  - `Adj Close`: Adjusted closing price (accounting for dividends and stock splits)
  - `Volume`: Shares traded during the session
- **Steps**:
  - Convert `Date` to datetime format.
  - Check for missing values and unique stocks.
  - Resample data if necessary to maintain consistency.

### 2. Exploratory Data Analysis (EDA)
- Check the time range of the dataset.
- Visualize trends in closing prices for each stock over the specified period.
  
### 3. Data Transformation for Stationarity
- Use **Augmented Dickey-Fuller (ADF)** tests to check for stationarity.
- Differencing was applied to make non-stationary series stationary.

### 4. Model Selection and Forecasting
- **Model**: Vector Auto Regression (VAR) model to capture relationships among multiple stocks.
- **Steps**:
  - Train the model on the stationary time series data.
  - Forecast future values over a specified time period.
  - Reverse differencing to obtain the forecasted values in their original scale.

### 5. Visualization
- Plot historical and forecasted closing prices for each stock to assess model predictions.

## Project Files

- `stocks.csv`: Historical stock data (not included here, use a sample stock data file).
- `multivariate_time_series_forecasting.py`: Main code file containing all steps described.
- `README.md`: This README file.

## Results

The model forecasts closing prices for each stock over a specified period, producing results in line with historical trends.

## Prerequisites

- Python 3.6 or above
- Required Libraries:
  ```bash
  pip install pandas matplotlib statsmodels
