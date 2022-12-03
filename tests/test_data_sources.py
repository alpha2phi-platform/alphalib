import unittest
import unittest.mock

import pandas as pd
import yfinance as yf

from alphalib.data_sources import nasdaq, seeking_alpha, yahoo_finance
from alphalib.utils.logger import logger

COUNTRY = "united states"


# For testing
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
# pd.set_option("display.max_colwidth", None)


class TestDataSources(unittest.TestCase):
    """Test out the different data sources."""

    stocks: pd.DataFrame

    def setUp(self):
        logger.info("Setup")

    def tearDown(self):
        logger.info("Tear down")

    def test_yf_get_stock_info(self):
        """Get stock info."""
        stock = yf.Ticker("BAC")
        stock_info = pd.DataFrame([stock.stats()])
        logger.info(stock_info.head(10).T)

    def test_seeking_alpha(self):
        stock_info = seeking_alpha.get_stock_info("GOOGL")
        print(stock_info)

    def test_yfinance(self):
        stock_info = yahoo_finance.get_stock_details("pmt")
        print(stock_info)

    def test_nasdaq_api(self):
        stock_info = nasdaq.get_stock_info("GOGL")
        print(stock_info)

    def test_nasdaq_browser(self):
        stock_info = nasdaq.get_stock_details("GOGL")
        print(stock_info)
