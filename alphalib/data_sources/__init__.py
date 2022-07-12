import investpy
import pandas as pd


def get_stock_countries() -> list[str]:
    """Get stock countries.

    Get supported countries.

    Returns:
        list[str]: A list of countries.
    """
    return investpy.stocks.get_stock_countries()


def get_stocks(country: str) -> pd.DataFrame:
    return investpy.stocks.get_stocks(country)
