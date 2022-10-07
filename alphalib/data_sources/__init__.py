# import investpy
from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from alphalib.utils import get_project_root
from .nasdaq import Nasdaq


@dataclass
class StockAnalysis:
    symbol: str = ""
    name: str = ""
    sector: str = ""
    exchange: str = ""
    currentPrice: float = 0
    earningsDate: datetime = datetime.min
    exDividendDate: datetime = datetime.min
    dividendDate: datetime = datetime.min
    dividendHistory: pd.DataFrame = pd.DataFrame()
    nasdaq: Nasdaq = Nasdaq()
    seeking_alpha: str = ""


def get_stocks() -> pd.DataFrame:
    stock_file = str(
        get_project_root()
        .absolute()
        .joinpath("".join(["data/stock", ".xlsx"]))
        .resolve()
    )
    return pd.read_excel(stock_file, sheet_name="stock")
