import unittest
import unittest.mock

import pandas as pd
from yahooquery import Ticker
import yahooquery as yq

from alphalib.dataset.yahooquery_downloader import Dataset

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
        symbol = "ADAP"
        ticker = Ticker(symbol)
        key_stats = ticker.key_stats[symbol]
        if isinstance(key_stats, dict):
            print(key_stats)
            print(ticker.quote_type)
            print(ticker.summary_profile)
            print(ticker.summary_detail)
        else:
            raise ValueError("Symbol {} is not found".format(symbol))

        ticker.session.close()
        self.assertGreater(len(key_stats), 0)

    def test_stock_stats(self):
        self.dataset.stock_stats()

    def test_news(self):
        result = yq.search("KEN")
        print(f" result: {str(result)}")  # __AUTO_GENERATED_PRINT_VAR__

    def test_multi_symbols(self):
        symbols = ["EFC", "OXLC"]
        for symbol in symbols:
            ticker = Ticker(symbol)
            key_stats = ticker.key_stats
            print(key_stats)
