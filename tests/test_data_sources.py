import unittest
import unittest.mock

import pandas as pd
import yfinance as yf

import alphalib.data_sources as ds
from alphalib.utils import logger

COUNTRY = "united states"


class TestDataSources(unittest.TestCase):
    """Test out the different data sources."""

    stocks: pd.DataFrame

    def setUp(self):
        logger.info("Setup")

    def tearDown(self):
        logger.info("Tear down")

    # def test_get_countries(self):
    #     self.countries = ds.get_stock_countries()
    #     logger.info(self.countries)

    # def test_get_stocks(self):
    #     self.stocks = ds.get_stocks(COUNTRY)
    #     logger.info(self.stocks.head(10))

    def test_yf_get_stock_info(self):
        """Get stock info."""
        stock = yf.Ticker("BAC")
        stock_info = pd.DataFrame([stock.info])
        logger.info(stock_info.head(10).T)
