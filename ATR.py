import pandas as pd
import numpy as np
"""
Current Industry Standard Period is 14 days.
"""


def ATR(data, period: int):
    data['High-Low'] = data['High'] - data['Low']
    data['High-PrevClose'] = abs(data['High'] - data['Close'].shift(1))
    data['Low-PrevClose'] = abs(data['Low'] - data['Close'].shift(1))

    data['TrueRange'] = data[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)

    # Calculate ATR as the moving average of TR over the specified period
    data['ATR'] = data['TrueRange'].rolling(window=period).mean()

    return data['ATR']
