import pandas as pd


def bollinger_bands(df, window=20, num_sd=2):

    rolling_mean = df['Close'].rolling(window).mean()
    rolling_std = df['Close'].rolling(window).std()

    df['mid'] = rolling_mean
    df['upper'] = rolling_mean + (rolling_std * num_sd)
    df['lower'] = rolling_mean - (rolling_std * num_sd)

    return df
