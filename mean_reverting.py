import numpy as np


def mean_reverting_strategy(data):
    """
    Mean-reverting strategy using Bollinger Bands and combined signals.

    Args:
        data (DataFrame): Data containing Bollinger Bands and combined signals.

    Returns:
        DataFrame: Updated DataFrame with generated signals.
    """
    data['Signal'] = np.where(
        (data['Combined_Signal'] == 1) & (data['Close'] < data['Lower Band']), 1,  # Buy
        np.where((data['Combined_Signal'] == -1) & (data['Close'] > data['Upper Band']), -1, 0)  # Sell
    )

    return data
