from datetime import datetime, timedelta
from typing import Tuple

import pandas as pd
from prophet import Prophet

from alphalib.analysis import get_historical_prices
from alphalib.utils.logging import logger

DAYS_AHEAD = 30
PAST_DAYS = 365 * 3


def prophet_predict(symbol: str) -> Tuple[pd.DataFrame, Prophet]:
    logger.info(f"Predicting prices for {symbol}")
    df_prices = get_historical_prices(
        symbol, datetime.now() - timedelta(days=PAST_DAYS), datetime.now()
    )

    # df_prices = pd.read_excel(f"data/{symbol}_historical_prices.xlsx")

    df_prices = df_prices[["date", "adjclose"]]
    df_prices["date"] = df_prices["date"].dt.date
    df_prices = df_prices.rename({"date": "ds", "adjclose": "y"}, axis="columns")

    m = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=True,
    )
    m.fit(df_prices)

    future_prices = m.make_future_dataframe(periods=DAYS_AHEAD)
    forecast_prices = m.predict(future_prices)

    return forecast_prices, m


def tsfresh_predict(symbol: str) -> pd.DataFrame:
    ...
    # TODO:


def tsflex_predict(symbol: str) -> pd.DataFrame:
    ...
    # TODO:
