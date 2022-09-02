import os
import time
import traceback
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import investpy
import pandas as pd
import yfinance as yf
from openpyxl import load_workbook
from rich import print as rprint
from rich.console import Console
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
        **to_excel_kwargs,
    ):
        # Excel file doesn't exist - saving and exiting
        if not os.path.isfile(filename):
            df.to_excel(
                filename,
                sheet_name=sheet_name,
                startrow=startrow if startrow is not None else 0,
                header=True,
                index=False,
                **to_excel_kwargs,
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
            writer,
            sheet_name,
            startrow=startrow,
            header=header,
            index=False,
            **to_excel_kwargs,
        )

        # save and close the workbook
        writer.save()
        writer.close()

    def _create_missing_cols(self, df, target_cols):
        columns = df.columns.tolist()
        missing_cols = list(set(target_cols) - set(columns))
        df[missing_cols] = None

    def download(self, continue_from_last_download=True, throttle=True) -> None:

        stocks = self.get_stocks()
        stocks_lookup = []
        stock_info_columns = []
        stock_dividends_columns = []
        stock_financials_columns = []

        if not continue_from_last_download:
            # Remove the exising file
            Path(self.file_name).unlink(missing_ok=True)
        else:
            if Path(self.file_name).exists():
                stock_info_download = pd.read_excel(
                    self.file_name,
                    sheet_name=self.SHEET_NAME_STOCK_INFO,
                    engine="openpyxl",
                )
                stock_financials_download = pd.read_excel(
                    self.file_name,
                    sheet_name=self.SHEET_NAME_STOCK_FINANCIALS,
                    engine="openpyxl",
                )
                stock_dividends_download = pd.read_excel(
                    self.file_name,
                    sheet_name=self.SHEET_NAME_STOCK_DIVIDENDS,
                    engine="openpyxl",
                )
                stocks_lookup = stock_info_download.symbol.tolist()
                stock_info_columns = stock_info_download.columns.tolist()
                stock_financials_columns = stock_financials_download.columns.tolist()
                stock_dividends_columns = stock_dividends_download.columns.tolist()
                stock_info_columns.sort()
                stock_financials_columns.sort()
                stock_dividends_columns.sort()

        # Get data for each stock
        console = Console()
        skip = False
        total_stocks = len(stocks)
        counter = 0
        last_10_years = datetime.now().year - 10
        with console.status(f"[bold green]Downloading stock..."):
            for stock in stocks.head(600).itertuples(index=False, name="Stock"):
                try:
                    skip = False
                    counter = counter + 1
                    if continue_from_last_download:
                        if stock.symbol in stocks_lookup:  # type: ignore
                            console.log(f"[blue]Skipping {stock.symbol}")  # type: ignore
                            skip = True
                            continue

                    ticker: Ticker = yf.Ticker(stock.symbol)  # type: ignore
                    history: pd.DataFrame = ticker.history()
                    if history.empty:
                        console.log(f"[blue]Stock not found. Skipping {stock.symbol}")  # type: ignore
                        continue

                    # Get stock data
                    stock_info = pd.DataFrame([ticker.info])
                    if len(stock_info_columns) == 0:
                        stock_info_columns = stock_info.columns.tolist()
                        stock_info_columns.sort()
                    if len(stock_info) > 0:
                        self._create_missing_cols(stock_info, stock_info_columns)

                    try:
                        # From investpy
                        stock_dividends = investpy.get_stock_dividends(stock.symbol, stock.country)  # type: ignore
                    except:
                        # From yfinance
                        stock_dividends = pd.DataFrame(ticker.dividends)
                        stock_dividends.reset_index(inplace=True)

                    stock_dividends["Country"] = stock.country  # type: ignore
                    stock_dividends["Name"] = stock.name  # type: ignore
                    stock_dividends["Symbol"] = stock.symbol  # type: ignore
                    stock_dividends["Full Name"] = stock.full_name  # type: ignore
                    if len(stock_dividends_columns) == 0:
                        stock_dividends_columns = stock_dividends.columns.tolist()
                        stock_dividends_columns.sort()
                    if len(stock_dividends) > 0:
                        self._create_missing_cols(
                            stock_dividends, stock_dividends_columns
                        )

                    stock_financials = ticker.financials.T  # type: ignore
                    stock_financials["Country"] = stock.country  # type: ignore
                    stock_financials["Name"] = stock.name  # type: ignore
                    stock_financials["Symbol"] = stock.symbol  # type: ignore
                    stock_financials["Full Name"] = stock.full_name  # type: ignore
                    stock_financials.index.name = "Date"
                    stock_financials.reset_index(inplace=True)
                    if len(stock_financials_columns) == 0:
                        stock_financials_columns = stock_financials.columns.tolist()
                        stock_financials_columns.sort()
                    if len(stock_financials) > 0:
                        self._create_missing_cols(
                            stock_financials, stock_financials_columns
                        )

                    if len(stock_dividends) > 0:
                        self._append_df_to_excel(
                            self.file_name,
                            stock_dividends[stock_dividends_columns][
                                pd.DatetimeIndex(stock_dividends["Date"]).year  # type: ignore
                                > last_10_years
                            ],
                            sheet_name="stock_dividends",
                        )

                    if len(stock_financials) > 0:
                        self._append_df_to_excel(
                            self.file_name,
                            stock_financials[stock_financials_columns],
                            sheet_name="stock_financials",
                        )

                    if len(stock_info) > 0:
                        self._append_df_to_excel(
                            self.file_name,
                            stock_info[stock_info_columns],
                            sheet_name="stock_info",
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
                        time.sleep(2)  # Sleep for x seconds
                except Exception as e:
                    rprint(f"Unable to download data for {stock.symbol}-{stock.name}", e)  # type: ignore
                    traceback.print_exc()
                    return
                finally:
                    if not skip:
                        console.log(f"[green]{counter}/{total_stocks} - Finish fetching data[/green] {stock.symbol}-{stock.name}")  # type: ignore
