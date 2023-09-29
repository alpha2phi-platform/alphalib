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
            hist_prices["date"], format="%Y-%m-%d %H:%M:%S%z", utc=True
        )
        return hist_prices
    except Exception as e:
        logger.error(f"Unable to retrieve historical prices for {symbol}", e)
        return pd.DataFrame()
    finally:
        ticker.session.close()


def get_earning_history(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    try:
        earning_history = ticker.earning_history
        return earning_history
    except Exception as e:
        logger.error(f"Unable to retrieve earning history for {symbol}", e)
        return pd.DataFrame()
    finally:
        ticker.session.close()


def get_fund_ownership(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    try:
        fund_ownership = ticker.fund_ownership
        return fund_ownership
    except Exception as e:
        logger.error(f"Unable to retrieve ownership for {symbol}", e)
        return pd.DataFrame()
    finally:
        ticker.session.close()


def get_institution_ownership(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    try:
        institution_ownership = ticker.institution_ownership
        return institution_ownership
    except Exception as e:
        logger.error(f"Unable to retrieve institution ownership for {symbol}", e)
        return pd.DataFrame()
    finally:
        ticker.session.close()


def get_recommendation_trend(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    try:
        recommendation_trend = ticker.recommendation_trend
        return recommendation_trend
    except Exception as e:
        logger.error(f"Unable to retrieve recommendation trend for {symbol}", e)
        return pd.DataFrame()
    finally:
        ticker.session.close()
