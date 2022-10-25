import unittest
import unittest.mock

import pandas as pd
import yfinance as yf

from alphalib.data_sources.nasdaq import get_stock_details as get_nasdaq
from alphalib.data_sources.seeking_alpha import \
    get_stock_details as get_seeking_alpha
from alphalib.data_sources.yahoo_finance import \
    get_stock_details as get_yfinance
from alphalib.dataset.high_yield import HighYield, get_high_yield_stocks
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

    def test_nasdaq(self):
        nasdaq = get_nasdaq("pmt")
        print(nasdaq)

    def test_seeking_alpha(self):
        seeking_alpha = get_seeking_alpha("GOGL")
        print(seeking_alpha)

    def test_yfinance(self):
        yahoo_finance = get_yfinance("pmt")
        print(yahoo_finance)

    def test_high_yield(self):
        stocks: list[HighYield] = get_high_yield_stocks()
        print(stocks)
        self.assertGreater(len(stocks), 0)
