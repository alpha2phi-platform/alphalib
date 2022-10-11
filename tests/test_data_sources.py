import unittest
import unittest.mock

import pandas as pd
import yfinance as yf

from alphalib.data_sources.nasdaq import get_stock_details as get_nasdaq
from alphalib.data_sources.seeking_alpha import \
    get_stock_details as get_seeking_alpha
from alphalib.data_sources.yahoo_finance import \
    get_stock_details as get_yfinance
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
        nasdaq = get_nasdaq("gogl")
        print(nasdaq)

    def test_seeking_alpha(self):
        seeking_alpha = get_seeking_alpha("T")
        print(seeking_alpha)

    def test_yfinance(self):
        yahoo_finance = get_yfinance("oxlc")
        print(yahoo_finance)
