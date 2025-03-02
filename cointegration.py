import numpy as np
from statsmodels.tsa.stattools import coint


def test_cointegration(series_a, series_b, significance_level=0.05):
    """
    Perform a cointegration test between two time series.

    Args:
        series_a (Series): First time series.
        series_b (Series): Second time series.
        significance_level (float): Significance level for the test.

    Returns:
        tuple: (bool, float) indicating whether the series are cointegrated and the p-value.
    """

    coint_score, p_value, _ = coint(series_a, series_b)
    is_cointegrated = p_value < significance_level

    return is_cointegrated, p_value
