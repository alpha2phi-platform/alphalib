import os
import pathlib
from dataclasses import dataclass
from enum import Enum

import pandas as pd
import yfinance as yf
from yfinance import Ticker

from alphalib.data_sources import get_stock_countries, get_stocks


class StorageFormat(Enum):
    EXCEL = 1
    PICKLE = 2


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
class Downloader:
    """Dataset downloader."""

    # Excel file name
    file_name = os.path.join(
        pathlib.Path(__file__).parent.parent.absolute(), "alphalib.xlsx"
    )

    # Default to US
    country: str = "united states"

    def __post_init__(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def get_countries() -> list[str]:
        """Get a list of countries."""
        return get_stock_countries()

    def _save(self, df: pd.DataFrame, sheet_name: str) -> None:
        """Save data to excel."""
        df.to_excel(
            self.file_name,
            sheet_name=sheet_name,
            header=True,
            index=False,
            na_rep="",
            engine="openpyxl",
        )

    def get_stocks(self) -> pd.DataFrame:
        """Retrieve all stocks."""
        return get_stocks(self.country)

    def get_stock_fundamentals(self, stock: tuple) -> None:

        # Fundamental analysis
        fa = FundamentalAnalysis(stock.country, stock.symbol)  # type: ignore

        # Get stock info
        stock_info = fa.get_info()
        print(stock_info.T)  # __AUTO_GENERATED_PRINT_VAR__

        # Get stock dividends
        # stock_dividends = fa.get_dividends()

        # Save the stock info
        # self._save(stock_info, "stock_info")

    def download( self, recoverable=True, show_progress=True, throttle=True) -> None:
        stocks = self.get_stocks()

        # Get data for each stock
        for row in stocks.head(1).itertuples(index=False, name="Stock"):
            self.get_stock_fundamentals(row)
