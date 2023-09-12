from datetime import datetime

import pandas as pd
from yahooquery import Ticker

from alphalib.utils.logging import logger


def get_historical_prices(
    symbol: str, start_date: datetime, end_date: datetime
) -> pd.DataFrame:
    ticker = Ticker(symbol)
    try:
        hist_prices = ticker.history(start=start_date, end=end_date)
        if hist_prices.empty:
            logger.error(f"Unable to retrieve historical prices for {symbol}")
            return pd.DataFrame()
        hist_prices.reset_index(inplace=True)
        hist_prices["date"] = pd.to_datetime(
            hist_prices["date"], format="%Y-%m-%d", utc=True
        ).dt.date
        return hist_prices
    except Exception as e:
        logger.error(f"Unable to retrieve historical prices for {symbol}", e)
        return pd.DataFrame()
    finally:
        ticker.session.close()
