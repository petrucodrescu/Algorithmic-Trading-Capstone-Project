import numpy as np


def calculate_adx(data, period=14):
    """
    Calculate the Average Directional Index (ADX) to measure trend strength.

    Args:
        data (DataFrame): Data containing 'High', 'Low', and 'Close' columns.
        period (int): Lookback period for ADX calculation.

    Returns:
        DataFrame: Updated DataFrame with 'ADX', 'DI+' and 'DI-' columns.
    """

    high_low = data['High'] - data['Low']
    high_close = abs(data['High'] - data['Close'].shift(1))
    low_close = abs(data['Low'] - data['Close'].shift(1))
    true_range = np.maximum.reduce([high_low, high_close, low_close])

    data['TR'] = true_range
    data['DM+'] = np.where((data['High'] - data['High'].shift(1)) > (data['Low'].shift(1) - data['Low']),
                           np.maximum(data['High'] - data['High'].shift(1), 0), 0)
    data['DM-'] = np.where((data['Low'].shift(1) - data['Low']) > (data['High'] - data['High'].shift(1)),
                           np.maximum(data['Low'].shift(1) - data['Low'], 0), 0)

    data['TR_SMA'] = data['TR'].rolling(window=period).mean()
    data['DI+'] = 100 * (data['DM+'] / data['TR_SMA'])
    data['DI-'] = 100 * (data['DM-'] / data['TR_SMA'])
    data['DX'] = 100 * abs(data['DI+'] - data['DI-']) / (data['DI+'] + data['DI-'])
    data['ADX'] = data['DX'].rolling(window=period).mean()

    return data[['ADX', 'DI+', 'DI-']]
