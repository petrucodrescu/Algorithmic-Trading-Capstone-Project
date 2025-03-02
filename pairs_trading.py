from mean_reverting import mean_reverting_strategy
from trend_following import trend_following_strategy


def pairs_trading_strategy(data):
    """
    Apply trading strategies based on detected market regimes.

    Args:
        data (DataFrame): Data containing regime labels and price data.

    Returns:
        DataFrame: Updated DataFrame with trading signals.
    """

    for regime in data['Regime'].unique():
        regime_data = data[data['Regime'] == regime]

        if regime == 0:  # Mean-reverting regime
            data.loc[regime_data.index] = mean_reverting_strategy(regime_data)
        elif regime == 1:  # Trend-following regime
            data.loc[regime_data.index] = trend_following_strategy(regime_data)

    return data
