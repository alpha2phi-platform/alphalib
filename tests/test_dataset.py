import unittest
import unittest.mock

import investpy
import pandas as pd
import yfinance as yf
from yfinance import Ticker

from alphalib.data_sources import get_stocks
from alphalib.dataset import Dataset
from alphalib.utils import logger

COUNTRY = "united states"
SYMBOL = "BAC"


# For testing
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
# pd.set_option("display.max_colwidth", None)


class TestDataset(unittest.TestCase):
    """Test out the fundamental indicator."""

    dataset = Dataset(country=COUNTRY)

    # All stock countries
    countries: list[str]

    # Stocks for a country
    stocks: pd.DataFrame

    def setUp(self):
        self.countries = Dataset.get_countries()
        self.stocks = self.dataset.get_stocks()

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
        print(stocks.head(1))

    def test_investpy_get_dividends(self):
        stock_dividends = investpy.get_stock_dividends(SYMBOL, COUNTRY)
        print(stock_dividends)

    def test_get_dataset(self):
        self.dataset.download(continue_from_last_download=True)
