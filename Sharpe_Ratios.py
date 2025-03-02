import pandas as pd
import numpy as np

import pandas as pd

def sharpe_ratio(data, risk_free_rate: float):
    equity_names = data.iloc[:, 0]
    prices = data.iloc[:, 1:]

    sharpe_dict = {}

    for equity in equity_names:
        price_series = prices[equity]

        returns = price_series.pct_change()

        # Calculating the Sharpe Ratio
        avg_return = returns.mean()
        std_dev_return = returns.std()

        sharpe = (avg_return - risk_free_rate) / std_dev_return if std_dev_return != 0 else None

        sharpe_dict[equity] = sharpe

    # Convert the dictionary to a DataFrame
    sharpe_df = pd.DataFrame(list(sharpe_dict.items()), columns=['Equity', 'Sharpe Ratio']).set_index('Equity')

    return sharpe_df
