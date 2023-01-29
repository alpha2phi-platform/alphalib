import unittest
import unittest.mock

import investpy
import pandas as pd
import yfinance as yf
from yfinance import Ticker

from alphalib.data_sources import get_stocks
from alphalib.dataset import Dataset, Downloader
from alphalib.utils.logger import logger

COUNTRY = "United States"
SYMBOL = "GOGL"


# For testing
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
# pd.set_option("display.max_colwidth", None)


class TestDataset(unittest.TestCase):
    dataset: Dataset

    def setUp(self):
        self.dataset = Dataset()

    def tearDown(self):
        logger.info("Tear down")

    def test_yfinance_get_dividends(self):
        ticker: Ticker = yf.Ticker("GOGL")
        ticker.history(period="10y")
        stock_dividends = ticker.dividends
        print(stock_dividends)

    def test_list_diff(self):
        a = ["a", "b", "c", "e"]
        b = ["a", "b", "c", "d"]
        c = list(set(b) - set(a))
        d = list(set(b).symmetric_difference(set(a)))
        print(len(c), c)
        print(len(d), d)

    def test_get_stocks(self):
        stocks = get_stocks()
        self.assertGreater(len(stocks), 0)

    def test_investpy_get_dividends(self):
        stock_dividends = investpy.get_stock_dividends(SYMBOL, COUNTRY)
        print(stock_dividends)

    def test_investpy_get_stock_info(self):
        stock_info = investpy.get_stock_information(SYMBOL, COUNTRY)
        print(stock_info.T)  # type: ignore

    def test_get_stock_info(self):
        self.dataset.stock_info()

    # def test_get_stock_financials(self):
    #     self.dataset.stock_financials()

    # def test_get_stock_dividends(self):
    #     self.dataset.stock_dividends()

    def test_get_stock_stats(self):
        self.dataset.stock_stats()

    def test_downloader(self):
        @Downloader(
            continue_last_download=True,
            file_prefix="alphalib_",
            sheet_name="stock_info",
            primary_col="symbol",
            throttle=2,
            start_pos=0,
        )
        def stock_info(*args, **kwargs):
            print("it works!")
            return pd.DataFrame()

        stock_info()

    def test_yfinance_get_stock_info(self):
        ticker: Ticker = yf.Ticker("SNPTY")
        print(ticker.info)

    def test_get_all_stats(self):
        ticker: Ticker = yf.Ticker(SYMBOL)
        stats = ticker.stats()
        for k, v in stats.items():
            if type(v) is dict:
                df = pd.DataFrame([v])
                print(f"---- {k} ----- ")
                print(df.head(1).T)

    def get_stats(self, stats, result, stats_type):
        if stats[stats_type]:
            v = stats[stats_type]
            if type(v) is dict:
                result = {**result, **v}
            return result

    def test_get_stats(self):
        ticker: Ticker = yf.Ticker(SYMBOL)
        stats = ticker.stats()
        result: dict = {}
        result = self.get_stats(stats, result, "defaultKeyStatistics")
        result = self.get_stats(stats, result, "financialData")
        result = self.get_stats(stats, result, "summaryDetail")
        df = pd.DataFrame([result])
        print(df.head(1).T)

    def test_yfinance_get_earning_dates(self):
        ticker: Ticker = yf.Ticker(SYMBOL)
        earning_dates = ticker.earnings_dates
        print(earning_dates)

    def test_yfinance_get_calendar(self):
        ticker: Ticker = yf.Ticker(SYMBOL)
        calendar = ticker.calendar
        print(calendar)
