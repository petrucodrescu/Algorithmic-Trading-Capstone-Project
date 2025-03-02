from statsmodels.api import OLS, add_constant


def calculate_hedging_ratio(series_a, series_b):
    """
    Calculate the hedging ratio between two time series using OLS regression.

    Args:
        series_a (Series): Dependent variable (e.g., Stock A prices).
        series_b (Series): Independent variable (e.g., Stock B prices).

    Returns:
        float: Hedging ratio (slope of the regression line).
    """

    series_b_with_constant = add_constant(series_b)
    model = OLS(series_a, series_b_with_constant).fit()

    return model.params[1]
