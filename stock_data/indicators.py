import pandas as pd

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
