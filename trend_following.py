import numpy as np


def trend_following_strategy(data):
    """
    Trend-following strategy using MACD, ADX, and combined signals.

    Args:
        data (DataFrame): Data containing MACD, ADX, and combined signals.

    Returns:
        DataFrame: Updated DataFrame with generated signals.
    """

    data['Signal'] = np.where(
        (data['Combined_Signal'] == 1) & (data['Close'] > data['EMA_200']), 1,  # Buy
        np.where((data['Combined_Signal'] == -1) & (data['Close'] < data['EMA_200']), -1, 0)  # Sell
    )

    return data
