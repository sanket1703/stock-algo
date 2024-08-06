from datetime import datetime, timedelta
import yfinance as yf


def fetch_stock_data(symbol):
    """
    Fetches historical stock data from Yahoo Finance API for a given symbol.

    Args:
        symbol (str): Stock symbol.

    Returns:
        pandas.DataFrame: Historical stock data.
    """
    stock_data = yf.download(symbol, period="11d", interval="1d")
    return stock_data

def fetch_1d_stock_data(symbol):
    """
    Fetches historical stock data from Yahoo Finance API for a given symbol.

    Args:
        symbol (str): Stock symbol.

    Returns:
        pandas.DataFrame: Historical stock data.
    """
    stock_data = yf.download(symbol, period="1d", interval="1d")
    return stock_data

def one_year_return(stocks):
    """
    Calculate the 1-year return of a given stock.

    Parameters:
    ticker (str): The stock ticker symbol.

    Returns:
    float: The 1-year return as a percentage.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=366)

    # Fetch historical data
    stock_data = yf.download(stocks, start=start_date, end=end_date)

    # Calculate the 1-year return
    start_price = stock_data['Close'].iloc[0]
    end_price = stock_data['Close'].iloc[-1]
    one_year_return = (end_price - start_price) / start_price * 100

    return one_year_return

def one_year_candles_return(ticker):
    """
    Calculate the 1-year return of the last 366 trading days of a given stock.

    Parameters:
    ticker (str): The stock ticker symbol.

    Returns:
    float: The 1-year return as a percentage.
    """
    # Define the period to cover more than 1 year (to ensure at least 366 trading days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=400)

    # Fetch historical data
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    # Ensure we only take the last 366 trading days
    stock_data = stock_data[-366:]

    # Display the fetched data to confirm it includes the last 366 trading days
    print(stock_data.head())
    print(stock_data.tail())

    # Calculate the 1-year return
    start_price = stock_data['Adj Close'].iloc[0]
    end_price = stock_data['Adj Close'].iloc[-1]
    one_year_return = (end_price - start_price) / start_price * 100

    return one_year_return


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