import pandas as pd
# import pandas_ta as ta

def calculate_ema(data, window=100):
    """
    Calculates the Exponential Moving Average (EMA) for a given dataset.

    Args:
        data (pandas.DataFrame): Historical stock data.
        window (int): Window size for EMA calculation.

    Returns:
        pandas.Series: EMA values.
    """
    #ema = data['Close'].ewm(span=window, min_periods=window).mean()
    # ema=ta.ema(data['Close'],window)
    ema = "ema"
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
    # supertrend = round(ta.supertrend(high=data['High'],low= data['Low'],close= data['Close'], length=10, multiplier=3)['SUPERT_10_3.0'],2)
    return "supertrend"
