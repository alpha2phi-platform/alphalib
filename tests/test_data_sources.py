import unittest
import unittest.mock
from datetime import datetime

import pandas as pd
import yfinance as yf

from alphalib.data_sources.nasdaq import get_dividend_history
from alphalib.utils.logger import logger

COUNTRY = "united states"


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
        stock_info = pd.DataFrame([stock.info])
        logger.info(stock_info.head(10).T)

    def test_method(self):
        print("\xa0 x17%x".strip(" $%\xa0"))

    def test_nasdaq(self):
        nasdaq = get_dividend_history("oxlc")
        print(nasdaq)
