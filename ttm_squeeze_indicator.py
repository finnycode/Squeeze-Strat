import pandas as pd


def ttm_squeeze(df, bb_window=20, kc_window=20, kc_multiplier=1.5):

    df['bb_middle_band'] = df['Close'].rolling(window=bb_window).mean()
    df['bb_stddev'] = df['Close'].rolling(window=bb_window).std()
    df['bb_upper_band'] = df['bb_middle_band'] + (df['bb_stddev'] * 2)
    df['bb_lower_band'] = df['bb_middle_band'] - (df['bb_stddev'] * 2)

    ma = df['Close'].rolling(window=kc_window).mean()
    range = df['High'].rolling(window=kc_window).max() - df['Low'].rolling(window=kc_window).min()
    df['kc_upper_band'] = ma + (range * kc_multiplier)
    df['kc_lower_band'] = ma - (range * kc_multiplier)

    df['ttm_squeeze'] = (df['bb_lower_band'] > df['kc_lower_band']).astype(int) - (
                df['bb_upper_band'] < df['kc_upper_band']).astype(int)

    return df
