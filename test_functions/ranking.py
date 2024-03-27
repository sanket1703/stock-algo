import yfinance as yf

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
    print(ema)
    return ema

def rank_stocks_by_ema_difference(stocks):
        """
        Ranks stocks based on the difference between the 100-day EMA and the last traded price.

        Args:
            stocks (list): List of stock symbols.

        Returns:
            list: Ranked list of stocks based on EMA difference.
        """
        ranked_stocks = []
        for symbol in stocks:
            data = fetch_stock_data(symbol)
            if data.empty:
                print(f"No data available for {symbol}.")
                continue
            ema = calculate_ema(data)
            last_traded_price = get_last_traded_price(data)
            ema_difference = abs(ema.iloc[-1] - last_traded_price)
            ranked_stocks.append((symbol, ema_difference))
        
        ranked_stocks.sort(key=lambda x: x[1])
        return ranked_stocks

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

# Example usage
if __name__ == "__main__":
    
    stocks = ['AAPL', 'GOOG', 'MSFT', 'AMZN']
    ranked_stocks = rank_stocks_by_ema_difference(stocks)
    print("Ranked stocks based on EMA difference:")
    for rank, (symbol, difference) in enumerate(ranked_stocks, start=1):
        print(f"{rank}. {symbol}: {difference}")
