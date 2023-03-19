import unittest
import unittest.mock

import pandas as pd

from alphalib.dataset.yahooquery_downloader import Dataset, Downloader
from yahooquery import Ticker

# For testing
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
# pd.set_option("display.max_colwidth", None)


class TestYahooQueryDownloader(unittest.TestCase):
    dataset: Dataset

    def setUp(self):
        self.dataset = Dataset()

    def test_yahooquery(self):
        ticker = Ticker("x12444")
        print(ticker.key_stats)

    def test_stock_stats(self):
        self.dataset.stock_stats()
