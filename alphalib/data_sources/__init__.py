# import investpy
from dataclasses import dataclass

import pandas as pd

from alphalib.utils import get_project_root

from .investing import Investing
from .nasdaq import Nasdaq
from .seeking_alpha import SeekingAlpha
from .yahoo_finance import YahooFinance


@dataclass
class AggregatedSource:
    name: str = ""
    symbol: str = ""
    sector: str = ""
    exchange: str = ""
    yahooFinance: YahooFinance = YahooFinance()
    investing: Investing = Investing()
    nasdaq: Nasdaq = Nasdaq()
    seeking_alpha: SeekingAlpha = SeekingAlpha()


def get_stocks() -> pd.DataFrame:
    stock_file = str(
        get_project_root()
        .absolute()
        .joinpath("".join(["data/stock", ".xlsx"]))
        .resolve()
    )
    return pd.read_excel(stock_file, sheet_name="stock")
