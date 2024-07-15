import yfinance as yf


def fetch_stock_data(symbol):
    """
    Fetches historical stock data from Yahoo Finance API for a given symbol.

    Args:
        symbol (str): Stock symbol.

    Returns:
        pandas.DataFrame: Historical stock data.
    """
    stock_data = yf.download(symbol, period="200d", interval="1d")
    return stock_data

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