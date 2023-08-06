import unittest
import unittest.mock

import pandas as pd
import yahooquery as yq
from yahooquery import Ticker

from alphalib.dataset.yahooquery_downloader import Dataset
from alphalib.utils.dateutils import days_interval_from_now, from_isoformat

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
        symbol = "OXLC"
        ticker = Ticker(symbol)
        key_stats = ticker.key_stats[symbol]
        if isinstance(key_stats, dict):
            print(key_stats)
            print(ticker.quote_type)
            print(ticker.summary_detail)
            print(ticker.summary_profile)
            print(ticker.calendar_events)
            print(ticker.financial_data)
            print(ticker.price)
        else:
            print(key_stats)
            raise ValueError("Symbol {} is not found".format(symbol))

        ticker.session.close()
        self.assertGreater(len(key_stats), 0)

    def test_sentiment_score(self):
        symbol = "aapl"
        ticker = Ticker(symbol)
        print(ticker.news)

    def test_stock_stats(self):
        self.dataset.stock_stats()

    def test_news(self):
        result = yq.search("KEN")
        print(f" result: {str(result)}")  # __AUTO_GENERATED_PRINT_VAR__

    def test_multi_symbols(self):
        symbols = ["OXLC"]
        for symbol in symbols:
            ticker = Ticker(symbol)
            key_stats = ticker.key_stats
            print(key_stats)

    def test_calculate_dividend_dt_interval(self):
        symbol = "OXLC"
        ticker = Ticker(symbol)
        exDividendDate = ticker.calendar_events[symbol].get("exDividendDate", None)
        if exDividendDate is not None:
            exDividendDate = from_isoformat(exDividendDate)
            print(exDividendDate)
            print(days_interval_from_now(exDividendDate))

        ticker.session.close()
        self.assertIsNotNone(exDividendDate)
