import pandas as pd
import requests


def request_data(ticker):
    data = requests.get(
        f'''https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/minute/2023-07-01/2023-07-07?adjusted=true&sort=asc&limit=50000&apiKey={key}''')
    data = data.json()
    data = data['results']
    data = pd.DataFrame(data)

    data = data.rename(columns={'o': 'Open', 'h': 'High', 'l': 'Low', 'c': 'Close', 'v': 'Volume'})

    data.to_csv('data.csv')

    return data


request_data('SPY')
