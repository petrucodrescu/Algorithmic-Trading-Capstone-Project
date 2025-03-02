import numpy as np
from cointegrated_pairs_strategy.spread import calculate_spread_and_signals
from cointegrated_pairs_strategy.cointegration import test_cointegration
from Signals.RSI Signals import RSI_signal
from Signals.ADX import calculate_adx
from Signals.ATR import ATR


def preprocess_pairs(data, stock_a_col, stock_b_col, rsi_weight=0.5, adx_weight=0.5):
    """
    Preprocess data for pairs trading, including cointegration testing, spread calculation,
    and signal generation using weighted RSI and ADX.

    Args:
        data (DataFrame): Data containing stock prices.
        stock_a_col (str): Column name for Stock A prices.
        stock_b_col (str): Column name for Stock B prices.
        rsi_weight (float): Weight assigned to RSI signals (0 to 1).
        adx_weight (float): Weight assigned to ADX signals (0 to 1).

    Returns:
        DataFrame: Updated DataFrame with spread, combined signals, and risk levels.
        float: Hedging ratio for the pair.
        bool: Whether the pair is cointegrated.
    """

    if stock_a_col not in data.columns or stock_b_col not in data.columns:
        raise KeyError(f"Columns '{stock_a_col}' and/or '{stock_b_col}' not found.")

    is_cointegrated, p_value = test_cointegration(data[stock_a_col], data[stock_b_col])
    if not is_cointegrated:
        raise ValueError(f"Pairs {stock_a_col} and {stock_b_col} not cointegrated (p-value={p_value:.4f}).")

    data = calculate_spread_and_signals(data, stock_a_col, stock_b_col)
    data['ATR'] = ATR(data, period=14)
    data['Stop Loss'] = data['Close'] - (1.5 * data['ATR'])
    data['Take Profit'] = data['Close'] + (1.5 * data['ATR'])
    data['RSI'] = RSI_signal(data)
    data['ADX'] = calculate_adx(data)['ADX']
    data['RSI_Signal'] = np.where(data['RSI'] < 30, 1, np.where(data['RSI'] > 70, -1, 0))
    data['ADX_Signal'] = np.where(data['ADX'] > 25, 1, 0)
    data['Combined_Signal'] = (rsi_weight * data['RSI_Signal'] + adx_weight * data['ADX_Signal']).round()

    return data, data['Spread'].iloc[-1], is_cointegrated
