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


def get_fund_top_holdings(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    try:
        fund_top_holdings = ticker.fund_top_holdings
        return fund_top_holdings
    except Exception as e:
        logger.error(f"Unable to retrieve holdings for {symbol}", e)
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


def get_grading_history(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    try:
        grading_history = ticker.grading_history
        return grading_history
    except Exception as e:
        logger.error(f"Unable to retrieve grading history for {symbol}", e)
        return pd.DataFrame()
    finally:
        ticker.session.close()


def get_insider_holders(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    try:
        insider_holders = ticker.insider_holders
        return insider_holders
    except Exception as e:
        logger.error(f"Unable to retrieve insider holders for {symbol}", e)
        return pd.DataFrame()
    finally:
        ticker.session.close()


def get_insider_transactions(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    try:
        insider_transactions = ticker.insider_transactions
        return insider_transactions
    except Exception as e:
        logger.error(f"Unable to retrieve insider transactions for {symbol}", e)
        return pd.DataFrame()
    finally:
        ticker.session.close()


def get_major_holders(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    try:
        major_holders = ticker.major_holders
        return pd.DataFrame.from_dict(major_holders, dtype=str)
    except Exception as e:
        logger.error(f"Unable to retrieve major holders for {symbol}", e)
        return pd.DataFrame()
    finally:
        ticker.session.close()


def get_page_views(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    try:
        page_views = ticker.page_views
        return pd.DataFrame.from_dict(page_views, dtype=str)
    except Exception as e:
        logger.error(f"Unable to retrieve page views for {symbol}", e)
        return pd.DataFrame()
    finally:
        ticker.session.close()


def get_share_purchase_activity(symbol: str) -> pd.DataFrame:
    ticker = Ticker(symbol)
    try:
        share_purchase_activity = ticker.share_purchase_activity
        return pd.DataFrame.from_dict(share_purchase_activity, dtype=str)
    except Exception as e:
        logger.error(f"Unable to retrieve share purchase activity for {symbol}", e)
        return pd.DataFrame()
    finally:
        ticker.session.close()
