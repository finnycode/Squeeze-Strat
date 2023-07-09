import pandas as pd
import numpy as np


def keltner_channel(df, window=20, multiplier=1.5):

    tp = (df['High'] + df['Low'] + df['Close']) / 3

    middle_line = tp.rolling(window=window).mean()

    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())

    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)

    atr = true_range.rolling(window=window).mean()

    upper_band = middle_line + (multiplier * atr)
    lower_band = middle_line - (multiplier * atr)

    df['high'] = upper_band
    df['mid'] = middle_line
    df['low'] = lower_band

    return df
