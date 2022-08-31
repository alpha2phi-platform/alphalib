import os
import time
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import yfinance as yf
from openpyxl import load_workbook
from yfinance import Ticker

from alphalib.data_sources import get_stock_countries, get_stocks
from alphalib.utils import get_project_root


@dataclass
class Dataset:
    """Dataset downloader."""

    country: str = "united states"
    file_name: str = ""

    SHEET_NAME_STOCK_INFO = "stock_info"
    SHEET_NAME_STOCK_DIVIDENDS = "stock_dividends"
    SHEET_NAME_STOCK_FINANCIALS = "stock_financials"

    def __post_init__(self):
        self.file_name = str(
            get_project_root()
            .absolute()
            .joinpath("".join(["alphalib_", self.country.replace(" ", "_"), ".xlsx"]))
            .resolve()
        )

    def __del__(self):
        pass

    @staticmethod
    def get_countries() -> list[str]:
        """Get a list of countries."""
        return get_stock_countries()

    def get_stocks(self) -> pd.DataFrame:
        """Retrieve all stocks."""
        return get_stocks(self.country)

    def _append_df_to_excel(
        self,
        filename,
        df: pd.DataFrame,
        sheet_name: str = "Sheet1",
        startrow: int | None = None,
        truncate_sheet: bool = False,
        **to_excel_kwargs
    ):
        # Excel file doesn't exist - saving and exiting
        if not os.path.isfile(filename):
            df.to_excel(
                filename,
                sheet_name=sheet_name,
                startrow=startrow if startrow is not None else 0,
                header=True,
                **to_excel_kwargs
            )
            return

        # ignore [engine] parameter if it was passed
        if "engine" in to_excel_kwargs:
            to_excel_kwargs.pop("engine")

        writer = pd.ExcelWriter(filename, engine="openpyxl", mode="a", if_sheet_exists="overlay")  # type: ignore

        # try to open an existing workbook
        writer.book = load_workbook(filename)  # type: ignore

        # get the last row in the existing Excel sheet
        # if it was not specified explicitly
        if startrow is None and sheet_name in writer.book.sheetnames:  # type: ignore
            startrow = writer.book[sheet_name].max_row  # type: ignore

        # truncate sheet
        if truncate_sheet and sheet_name in writer.book.sheetnames:  # type: ignore
            # index of [sheet_name] sheet
            idx = writer.book.sheetnames.index(sheet_name)  # type: ignore
            # remove [sheet_name]
            writer.book.remove(writer.book.worksheets[idx])  # type: ignore
            # create an empty sheet [sheet_name] using old index
            writer.book.create_sheet(sheet_name, idx)  # type: ignore

        # copy existing sheets
        writer.sheets = {ws.title: ws for ws in writer.book.worksheets}  # type: ignore

        if startrow is None:
            startrow = 0

        header = False
        if startrow == 0:
            header = True

        # write out the new sheet
        df.to_excel(
            writer, sheet_name, startrow=startrow, header=header, **to_excel_kwargs
        )

        # save and close the workbook
        writer.save()
        writer.close()

    def download(
        self, continue_from_last_download=True, show_progress=True, throttle=True
    ) -> None:

        stocks = self.get_stocks()
        stocks_lookup = []

        if not continue_from_last_download:
            # Remove the exising file
            Path(self.file_name).unlink(missing_ok=True)
        else:
            if Path(self.file_name).exists():
                df_download = pd.read_excel(
                    self.file_name,
                    sheet_name=self.SHEET_NAME_STOCK_INFO,
                    engine="openpyxl",
                )
                stocks_lookup = df_download.symbol.tolist()

        # Get data for each stock
        for stock in stocks.head(2).itertuples(index=False, name="Stock"):

            if continue_from_last_download:
                if stock.symbol in stocks_lookup: # type: ignore
                    print(f"Skipping {stock.symbol}") # type: ignore
                    continue
                    
            
            ticker: Ticker = yf.Ticker(stock.symbol)  # type: ignore

            # Get stock data
            stock_info = pd.DataFrame([ticker.info])

            stock_dividends = pd.DataFrame(ticker.dividends)
            stock_dividends["Country"] = stock.country  # type: ignore
            stock_dividends["Name"] = stock.name  # type: ignore
            stock_dividends["Symbol"] = stock.symbol  # type: ignore
            stock_dividends["Full Name"] = stock.full_name  # type: ignore

            stock_financials = ticker.financials.T  # type: ignore
            stock_financials["Country"] = stock.country  # type: ignore
            stock_financials["Name"] = stock.name  # type: ignore
            stock_financials["Symbol"] = stock.symbol  # type: ignore
            stock_financials["Full Name"] = stock.full_name  # type: ignore
            stock_financials.index.name = "Date"

            if len(stock_dividends) > 0:
                self._append_df_to_excel(
                    self.file_name,
                    stock_dividends,
                    sheet_name="stock_dividends",
                )

            if len(stock_financials) > 0:
                self._append_df_to_excel(
                    self.file_name,
                    stock_financials,
                    sheet_name="stock_financials",
                )

            if len(stock_info) > 0:
                self._append_df_to_excel(
                    self.file_name,
                    stock_info,
                    sheet_name="stock_info",
                    index=False,
                )

            # stock_cashflow = ticker.cashflow
            # stock_earnings = ticker.earnings
            # stock_balance_sheet = ticker.balance_sheet
            # stock_calendar = ticker.calendar
            # stock_earnings_date  = ticker.earnings_dates
            # stock_recommendations = ticker.recommendations
            # stock_news = ticker.news
            # stock_history = ticker.history()
            # stock_splits = ticker.splits
            # stock_earnings_history = ticker.earnings_history
            # stock_actions = ticker.actions
            # stock_analysis = ticker.analysis
            # stock_stats = ticker.stats()
            # stock_sustainability = ticker.sustainability

            if throttle:
                time.sleep(3)  # Sleep for 3 seconds
