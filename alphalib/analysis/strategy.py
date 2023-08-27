import pandas as pd
from yahooquery import Ticker
from alphalib.utils.convertutils import join_dicts


def recent_prices(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    data = pd.DataFrame()
    try:
        data = ticker.history(period="1y")

        _14_low = data.tail(14)["close"].min()
        _14_high = data.tail(14)["close"].max()
        _14_mean = data.tail(14)["close"].mean()
        print("14 days", _14_low, _14_high, _14_mean)

        _30_low = data.tail(30)["close"].min()
        _30_high = data.tail(30)["close"].max()
        _30_mean = data.tail(30)["close"].mean()
        print("30 days", _30_low, _30_high, _30_mean)

        _60_low = data.tail(60)["close"].min()
        _60_high = data.tail(60)["close"].max()
        _60_mean = data.tail(60)["close"].mean()
        print("60 days", _60_low, _60_high, _60_mean)

        result: dict = {}
        key_stats = ticker.key_stats
        result = join_dicts(result, key_stats, symbol)
        result = join_dicts(result, ticker.quote_type, symbol)
        result = join_dicts(result, ticker.summary_detail, symbol)
        result = join_dicts(result, ticker.summary_profile, symbol)
        result = join_dicts(result, ticker.calendar_events, symbol)
        result = join_dicts(result, ticker.financial_data, symbol)
        result = join_dicts(result, ticker.price, symbol)
        print(result)

        eps = result["forwardEps"]
        pe_ratio = result["forwardPE"]
        current_price = result["currentPrice"]
        target_price = eps * pe_ratio
        print(f"EPS - {eps}, PE - {pe_ratio}")
        print(f"The current price is ${target_price:.2f}")
        print(f"The target price is ${target_price:.2f}")

        # https://learn.robinhood.com/articles/3V1482W9HFbJScuUHDaCqN/what-is-a-price-target/
        # Price target = (Current PE ratio / Forward PE ratio) x Current Price

        return data
    finally:
        ticker.session.close()
    return data
