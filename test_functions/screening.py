import yfinance as yf
import pandas as pd
import pandas_ta as ta

def fetch_stock_data(symbol):
    """
    Fetches historical stock data from Yahoo Finance API for a given symbol.

    Args:
        symbol (str): Stock symbol.

    Returns:
        pandas.DataFrame: Historical stock data.
    """
    stock_data = yf.download(symbol, period="200d", interval="1d")
    # print(stock_data)
    return stock_data

def calculate_ema(data, window=100):
    """
    Calculates the Exponential Moving Average (EMA) for a given dataset.

    Args:
        data (pandas.DataFrame): Historical stock data.
        window (int): Window size for EMA calculation.

    Returns:
        pandas.Series: EMA values.
    """
    ema = data['Close'].ewm(span=window, min_periods=window).mean()
    return ema

def calculate_supertrend(data, window=7, multiplier=3):
    """
    Calculates the Supertrend indicator for a given dataset.

    Args:
        data (pandas.DataFrame): Historical stock data.
        window (int): Window size for ATR calculation.
        multiplier (int): Multiplier for ATR calculation.

    Returns:
        pandas.Series: Supertrend values.
    """
    supertrend = round(ta.supertrend(high=data['High'],low= data['Low'],close= data['Close'], length=10, multiplier=3)['SUPERT_10_3.0'],2)
    return supertrend

def get_last_traded_price(data):
    """
    Retrieves the last traded price from historical stock data.

    Args:
        data (pandas.DataFrame): Historical stock data.

    Returns:
        float: Last traded price.
    """
    last_traded_price = data['Close'].iloc[-1]
    return last_traded_price

def filter_stocks(stocks):
    """
    Filters stocks based on specified conditions.

    Args:
        stocks (list): List of stock symbols.

    Returns:
        list: Filtered list of stocks.
    """
    filtered_stocks = []
    for symbol in stocks:
        data = fetch_stock_data(symbol)
        if data.empty:
            print(f"No data available for {symbol}.")
            continue
        ema = calculate_ema(data)
        last_traded_price = data['Close'].iloc[-1]
        supertrend = calculate_supertrend(data)
        if last_traded_price > 1.03 * ema.iloc[-1] and last_traded_price > supertrend.iloc[-1]:
            filtered_stocks.append(symbol)
    return filtered_stocks

# Example usage
if __name__ == "__main__":
    stocks = ['INDHOTEL.NS']
    filtered_stocks = filter_stocks(stocks)
    print("Filtered stocks based on conditions:")
    print(filtered_stocks)
