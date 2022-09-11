import unittest
import unittest.mock

import investpy
import pandas as pd
import yfinance as yf
from yfinance import Ticker

from alphalib.data_sources import get_stocks
from alphalib.dataset import Dataset, Downloader
from alphalib.utils import logger

COUNTRY = "united states"
SYMBOL = "T"


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

    def test_get_ticker(self):
        # ticker: Ticker = yf.Ticker("GM")
        # stock_dividends = ticker.dividends
        # print(stock_dividends)
        stock_dividends = investpy.get_stock_dividends("NSP", COUNTRY)
        print(stock_dividends)

    def test_list_diff(self):
        a = ["a", "b", "c", "e"]
        b = ["a", "b", "c", "d"]
        c = list(set(b) - set(a))
        d = list(set(b).symmetric_difference(set(a)))
        print(c)
        print(d)

    def test_get_stocks(self):
        stocks = get_stocks(COUNTRY)
        self.assertGreater(len(stocks), 0)

    def test_investpy_get_dividends(self):
        stock_dividends = investpy.get_stock_dividends(SYMBOL, COUNTRY)
        print(stock_dividends)

    def test_investpy_get_stock_info(self):
        stock_info = investpy.get_stock_information(SYMBOL, COUNTRY)
        print(stock_info.T)

    def test_get_stock_info(self):
        self.dataset.stock_info()

    def test_get_stock_dividends(self):
        self.dataset.stock_dividends()

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
