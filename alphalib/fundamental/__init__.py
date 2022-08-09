import os
import pathlib
import sqlite3
from dataclasses import dataclass, field

import pandas as pd
import yfinance as yf
from yfinance import Ticker

from alphalib.data_sources import get_stock_countries, get_stocks


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

    # Default to US
    country: str = "united states"

    # Indicators
    indicators: list[FundamentalIndicator] = field(default_factory=list)

    # Fundamamental analysis
    fa: FundamentalAnalysis = field(init=False)

    def __post_init__(self):
        pass

    @staticmethod
    def get_countries() -> list[str]:
        """Get a list of countries."""
        return get_stock_countries()

    def get_stocks(self) -> pd.DataFrame:
        """Retrieve all stocks."""
        return get_stocks(self.country)

    def get_fundamentals(self) -> None:
        stocks = self.get_stocks()
        # self.fa = FundamentalAnalysis(self.country, symbol)
        # print(self.fa.get_info())

    # def load(self):
    #     """Load existing analysis."""
    #     db = sqlite3.connect(self.db_name)

    # def save(self):
    #     """Save analysis to db."""
    #     db = sqlite3.connect(self.db_name)  # Create the db if does not exist
