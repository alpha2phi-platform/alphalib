import unittest
import unittest.mock

import investpy
import pandas as pd

from alphalib.fundamental import FundamentalAnalysis, MarketAnalysis
from alphalib.models import Stock
from alphalib.utils import logger

COUNTRY = "united states"
SYMBOL = "BAC"


class TestFundamental(unittest.TestCase):
    """Test out the fundamental indicator."""

    ma = MarketAnalysis(country=COUNTRY)
    fa = FundamentalAnalysis(country=COUNTRY, symbol=SYMBOL)

    # All stock countries
    countries: list[str]

    # Stocks for a country
    stocks: pd.DataFrame

    # Info for a stock
    stock: Stock

    def setUp(self):
        self.countries = MarketAnalysis.get_countries()
        self.stocks = self.ma.get_stocks()

    def tearDown(self):
        logger.info("Tear down")

    def test_get_stock_info(self):
        stock_info = self.fa.get_info()
        self.assertGreater(len(stock_info), 0)
        cols = [
            "yield",
            "forwardEps",
            "forwardPE",
            "pegRatio",
            "trailingEps",
            "trailingPE",
            "trailingPegRatio",
            "freeCashflow",
        ]
        indicators = stock_info[cols]
        logger.info(indicators.T)

    def test_investpy_get_info(self):
        stock_info = investpy.get_stock_information(SYMBOL, COUNTRY)
        logger.info(stock_info.T)

    def test_get_stocks_financials(self):
        financials = self.fa.get_financials()
        self.assertGreater(len(financials), 0)
        logger.info(financials)

    def test_get_dividends(self):
        dividends = self.fa.get_dividends()
        self.assertGreater(len(dividends), 0)
        logger.info(dividends.head(10))

    def test_get_fundamentals(self):
        self.ma.download_fundamentals()
