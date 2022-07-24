import investpy
import pandas as pd

from ..utils import logger


def get_stock_info(country, symbol) -> pd.DataFrame:
    try:
        stock_info = investpy.get_stock_information(symbol, country)
        stock_info["country"] = country
        return stock_info
    except Exception as e:
        logger.exception(f"Error getting stock for {country} - {symbol}", e)
        return pd.DataFrame()


def get_stock_dividends(country, symbol) -> pd.DataFrame:
    try:
        return investpy.get_stock_dividends(symbol, country)
    except Exception as e:
        logger.exception(f"Error getting stock for {country} - {symbol}", e)
        return pd.DataFrame()
