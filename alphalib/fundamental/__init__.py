import os
import pathlib
import sqlite3
from dataclasses import dataclass, field
from sqlite3 import dbapi2

import pandas as pd
import yfinance as yf
from yfinance import Ticker

from alphalib.data_sources import get_stock_countries, get_stocks
from alphalib.utils import logger


@dataclass
class FundamentalIndicator:
    pass


@dataclass
class FundamentalAnalysis:
    """Perform fundamental analysis for stocks."""

    # Country
    country: str

    # Symbol
    symbol: str

    # Stock
    stock: Ticker

    def __init__(self, country: str, symbol: str):
        """Constructor.

        Args:
            country (str): Country
            symbol (str): Stock symbol
        """
        self.country = country
        self.symbol = symbol
        self.stock = yf.Ticker(symbol)

    def get_info(self) -> pd.DataFrame:
        return pd.DataFrame([self.stock.info])

    def get_financials(self) -> pd.DataFrame:
        return self.stock.financials  # type: ignore

    def get_dividends(self) -> pd.DataFrame:
        return pd.DataFrame(self.stock.dividends).reset_index()


@dataclass
class MarketAnalysis:
    """Analyse a market."""

    # sqlite db name
    db_name = os.path.join(
        pathlib.Path(__file__).parent.parent.absolute(), "alphalib.db"
    )

    db: dbapi2.Connection = field(init=False)

    # Default to US
    country: str = "united states"

    # Indicators
    indicators: list[FundamentalIndicator] = field(default_factory=list)

    # Fundamamental analysis
    # fa: FundamentalAnalysis = field(init=False)

    def __post_init__(self):
        self.db = sqlite3.connect(self.db_name)

    def __del__(self):
        self.db.close()

    @staticmethod
    def get_countries() -> list[str]:
        """Get a list of countries."""
        return get_stock_countries()

    @staticmethod
    def get_stock_fundamentals(stock: pd.Series) -> None:
        # country, name, full_name, isin, currency, symbol
        fa = FundamentalAnalysis(stock.country, stock.symbol)
        flds = stock.keys().to_list()
        stock_info = fa.get_info()
        stock_info[flds] = stock[flds]
        
        

    def get_stocks(self) -> pd.DataFrame:
        """Retrieve all stocks."""
        return get_stocks(self.country)

    def download_fundamentals(self) -> None:
        stocks = self.get_stocks()
        stocks.head(1).apply(MarketAnalysis.get_stock_fundamentals, axis=1)
