import unittest
import unittest.mock

import pandas as pd

import alphalib.data_sources as ds
from alphalib.data_sources import investing
from alphalib.utils import logger

COUNTRY = "united states"


class TestDataSources(unittest.TestCase):
    """Test out the different data sources.
    """

    stocks: pd.DataFrame

    def setUp(self):
        logger.info("Setup")

    def tearDown(self):
        logger.info("Tear down")

    def test_investing_get_stocks(self):
        self.stocks = ds.get_stocks(COUNTRY)
        logger.info(self.stocks.head(10))

    def test_investing_get_stock_info(self):
        stock_info = investing.get_stock_info(COUNTRY, "AAPL")
        logger.info(stock_info.head(10).T)

    def test_investing_get_stock_dividends(self):
        stock_dividends = investing.get_stock_dividends(COUNTRY, "AAPL")
        logger.info(stock_dividends.head(10))
