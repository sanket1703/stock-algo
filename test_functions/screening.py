import yfinance as yf
import pandas as pd

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
    tr1 = data['High'] - data['Low']
    tr2 = abs(data['High'] - data['Close'].shift())
    tr3 = abs(data['Low'] - data['Close'].shift())
    true_range = pd.DataFrame({'TR1': tr1, 'TR2': tr2, 'TR3': tr3}).max(axis=1)
    atr = true_range.rolling(window=window).mean()
    basic_upper_band = (data['High'] + data['Low']) / 2 + multiplier * atr
    basic_lower_band = (data['High'] + data['Low']) / 2 - multiplier * atr
    super_trend = pd.Series(index=data.index)
    super_trend.iloc[0] = data['Close'].iloc[0]
    for i in range(1, len(data)):
        if super_trend.iloc[i-1] <= basic_upper_band.iloc[i-1]:
            super_trend.iloc[i] = basic_upper_band.iloc[i]
        else:
            super_trend.iloc[i] = basic_lower_band.iloc[i]
    return super_trend

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
    stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN','AUROPHARMA.NS']
    filtered_stocks = filter_stocks(stocks)
    print("Filtered stocks based on conditions:")
    print(filtered_stocks)
