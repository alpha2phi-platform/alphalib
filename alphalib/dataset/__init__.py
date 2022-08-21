import os
import pathlib
from dataclasses import dataclass

import pandas as pd
import yfinance as yf
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from yfinance import Ticker

from alphalib.data_sources import get_stock_countries, get_stocks


@dataclass
class Dataset:
    """Dataset downloader."""

    TARGET_FILE_NAME = os.path.join(
        pathlib.Path(__file__).parent.parent.absolute(), "alphalib.xlsx"
    )

    RECOVERY_FILE = os.path.join(
        pathlib.Path(__file__).parent.parent.absolute(), "recovery.txt"
    )

    country: str = "united states"

    def __post_init__(self):
        pass

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
        startrow=None,
        truncate_sheet=False,
        **to_excel_kwargs
    ):
        # Excel file doesn't exist - saving and exiting
        if not os.path.isfile(filename):
            df.to_excel(
                filename,
                sheet_name=sheet_name,
                startrow=startrow if startrow is not None else 0,
                **to_excel_kwargs
            )
            return

        # ignore [engine] parameter if it was passed
        if "engine" in to_excel_kwargs:
            to_excel_kwargs.pop("engine")

        writer: pd.ExcelWriter = pd.ExcelWriter(filename, engine="openpyxl", mode="a")  # type: ignore

        # try to open an existing workbook
        writer.book = load_workbook(filename)

        # get the last row in the existing Excel sheet
        # if it was not specified explicitly
        if startrow is None and sheet_name in writer.book.sheetnames:
            startrow = writer.book[sheet_name].max_row

        # truncate sheet
        if truncate_sheet and sheet_name in writer.book.sheetnames:
            # index of [sheet_name] sheet
            idx = writer.book.sheetnames.index(sheet_name)
            # remove [sheet_name]
            writer.book.remove(writer.book.worksheets[idx])
            # create an empty sheet [sheet_name] using old index
            writer.book.create_sheet(sheet_name, idx)

        # copy existing sheets
        writer.sheets = {ws.title: ws for ws in writer.book.worksheets}

        if startrow is None:
            startrow = 0

        # write out the new sheet
        df.to_excel(writer, sheet_name, startrow=startrow, **to_excel_kwargs)

        # save the workbook
        writer.save()

    def download(self, recoverable=True, show_progress=True, throttle=True) -> None:
        stocks = self.get_stocks()

        # Get data for each stock
        for stock in stocks.head(2).itertuples(index=False, name="Stock"):
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

            with pd.ExcelWriter(self.TARGET_FILE_NAME, engine="openpyxl", mode="w") as writer:  # type: ignore
                stock_info.to_excel(
                    writer, sheet_name="stock_info", index=False, header=True
                )
                stock_dividends.to_excel(
                    writer, sheet_name="stock_dividends", header=True
                )
                stock_financials.to_excel(
                    writer, sheet_name="stock_financials", header=True
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

            # Save the stock info
