"""Note on Usage and Generalizability.

Usage:
    This function takes in a dataframe of which the first column is the name of the
equity and the rest being prices RECORDED FOR OUR CHOSEN TIME FRAME.
I.e if we have a dataframe, one row can be for AMZN, while the rest of the
columns represent the new/recent prices for every 3 minutes as an example.

Generalizability:
    The main goal for generalizability is to make it update in real time with
the most recent data. (and further development but not recommended on this
function is to create the signal on when the RSI tells us to buy or sell can
be changed by us as we tweak our model.)
"""


import pandas as pd
import numpy as np

def RSI_signal(data, period: int = 14):
    equity_names = data.iloc[:, 0]
    prices = data.iloc[:, 1:]

    rsi_df = pd.DataFrame(index=prices.columns, columns=equity_names)

    for equity in equity_names:
        price_series = prices.loc[equity]

        #Price Computations
        delta = price_series.diff()

        gains = np.where(delta > 0, delta, 0)
        losses = np.where(delta < 0, -delta, 0)

        avg_gain = pd.Series(gains).rolling(window=period, min_periods=1).mean()
        avg_loss = pd.Series(losses).rolling(window=period, min_periods=1).mean()

        # Calculate RS
        rs = avg_gain / avg_loss

        # Calculate RSI
        rsi = 100 - (100 / (1 + rs))

        rsi_df[equity] = rsi.values

    return rsi_df
