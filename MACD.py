import pandas as pd
import numpy as np
"""
The industry standard is the short period being 12 days long, the long period
being 26 days, and the signal period being 9 days.
"""


def MACD(data, short_period: int, long_period: int, signal_period: int):
    
    data['EMA_Short'] = data['Close'].ewm(span=short_period, min_periods=1, adjust=False).mean()
    data['EMA_Long'] = data['Close'].ewm(span=long_period, min_periods=1, adjust=False).mean()

    # MACD Calculations
    data['MACD'] = data['EMA_Short'] - data['EMA_Long']
    data['Signal_Line'] = data['MACD'].ewm(span=signal_period, min_periods=1, adjust=False).mean()
    data['Histogram'] = data['MACD'] - data['Signal_Line']

    return data[['MACD', 'Signal_Line', 'Histogram']]
