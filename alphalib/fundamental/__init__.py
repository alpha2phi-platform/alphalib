import os
import pathlib
import sqlite3
from dataclasses import dataclass, field

import pandas as pd
import yfinance as yf
from yfinance import Ticker

from alphalib.data_sources import get_stock_countries, get_stocks
from alphalib.utils import logger


@dataclass
class FundamentalIndicator:
    pass


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

    @staticmethod
    def get_countries() -> list[str]:
        """Get a list of countries."""
        return get_stock_countries()

    def get_stocks(self) -> pd.DataFrame:
        """Retrieve all stocks."""
        return get_stocks(self.country)

    def load(self):
        """Load existing analysis."""
        db = sqlite3.connect(self.db_name)

    def save(self):
        """Save analysis to db."""
        db = sqlite3.connect(self.db_name)  # Create the db if does not exist


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

    def get_financials(self)-> pd.DataFrame:
        """Financial info."""
        return pd.DataFrame(self.stock.financials)

    def get_info(self) -> pd.DataFrame:
        """Stock info."""
        # logger.info(self.stock.info)
        return pd.DataFrame([self.stock.info])
