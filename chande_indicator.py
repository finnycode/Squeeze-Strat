import pandas as pd


def calculate_cmo(data, period=14):

    delta = data['Close'].diff()

    gains = delta.where(delta > 0, 0.0)
    losses = -delta.where(delta < 0, 0.0)

    gains_sum = gains.rolling(period).sum()
    losses_sum = losses.rolling(period).sum()

    cmo = 100 * (gains_sum - losses_sum) / (gains_sum + losses_sum)

    return cmo



