import numpy as np


def calculate_spread_and_signals(data, stock_a_col, stock_b_col, hedging_ratio):
    """
    Calculate the spread between two stocks and generate trading signals.

    Args:
        data (DataFrame): Data containing price columns for stocks.
        stock_a_col (str): Column name for Stock A prices.
        stock_b_col (str): Column name for Stock B prices.
        hedging_ratio (float): Hedging ratio between Stock A and Stock B.

    Returns:
        DataFrame: Updated DataFrame with calculated spread and trading signals.
    """

    data['Spread'] = data[stock_a_col] - (hedging_ratio * data[stock_b_col])
    spread_mean = data['Spread'].mean()
    spread_std = data['Spread'].std()

    data['Signal'] = 0
    data.loc[data['Spread'] > spread_mean + 2 * spread_std, 'Signal'] = -1  # Short
    data.loc[data['Spread'] < spread_mean - 2 * spread_std, 'Signal'] = 1   # Long

    return data
