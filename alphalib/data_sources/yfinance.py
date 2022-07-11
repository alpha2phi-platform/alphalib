import pandas as pd
import yfinance

from ..utils import logger


def get_stock_countries() -> list[str]:
    """Get stock countries.

    Get supported countries.

    Returns:
        list[str]: A list of countries.
    """
    return yfinance.
