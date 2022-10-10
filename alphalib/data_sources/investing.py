from dataclasses import dataclass

import investpy
import pandas as pd


@dataclass
class Investing:
    symbol: str = ""
    dividend_history: pd.DataFrame = pd.DataFrame()


def get_stock_details(symbol: str, country: str = "united states") -> Investing:
    assert symbol is not None
    investing = Investing()
    investing.symbol = symbol
    try:
        investing.dividend_history = investpy.get_stock_dividends(symbol, country)
    except Exception:
        investing.dividend_history = pd.DataFrame()
    return investing
