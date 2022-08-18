import os
import pathlib
from dataclasses import dataclass
from enum import Enum

import pandas as pd
import yfinance as yf
from yfinance import Ticker

from alphalib.data_sources import get_stock_countries, get_stocks


class Storage(Enum):
    EXCEL = 1
    PICKLE = 2


@dataclass
class Dataset:
    """Dataset downloader."""

    # Excel file name
    file_name = os.path.join(
        pathlib.Path(__file__).parent.parent.absolute(), "alphalib.xlsx"
    )

    # Default to US
    country: str = "united states"

    # Storage
    storage: Storage = Storage.EXCEL

    def __post_init__(self):
        if self.storage == Storage.PICKLE:
            self.file_name = os.path.join(
                pathlib.Path(__file__).parent.parent.absolute(), "alphalib.pkl"
            )

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

    def download(self, recoverable=True, show_progress=True, throttle=True) -> None:
        stocks = self.get_stocks()

        # Get data for each stock
        for stock in stocks.head(1).itertuples(index=False, name="Stock"):
            ticker: Ticker = yf.Ticker(stock.symbol)  # type: ignore

            # Get stock info
            stock_info = pd.DataFrame([ticker.info])
            print(stock_info.T)

            # Get stock dividends
            stock_dividends = pd.DataFrame(ticker.dividends).reset_index()
            print(stock_dividends.T)

            # Save the stock info
            self._save(stock_info, "stock_info")

