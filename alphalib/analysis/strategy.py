import pandas as pd
from yahooquery import Ticker


def recent_prices(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    data = pd.DataFrame()
    try:
        data = ticker.history(period="1y")

        _14_low = data.tail(14)["close"].min()
        _14_high = data.tail(14)["close"].max()
        _14_mean = data.tail(14)["close"].mean()
        print(_14_low, _14_high, _14_mean)

        _30_low = data.tail(30)["close"].min()
        _30_high = data.tail(30)["close"].max()
        _30_mean = data.tail(30)["close"].mean()
        print(_30_low, _30_high, _30_mean)

        _60_low = data.tail(60)["close"].min()
        _60_high = data.tail(60)["close"].max()
        _60_mean = data.tail(60)["close"].mean()
        print(_60_low, _60_high, _60_mean)

        # eps = 3.50
        # pe_ratio = 20
        # target_price = eps * pe_ratio
        # print(f"The target price is ${target_price:.2f}")

        return data
    finally:
        ticker.session.close()
    return data
