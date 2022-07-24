import unittest
import unittest.mock

import pandas as pd

from alphalib.fundamental import FundamentalAnalysis, MarketAnalysis
from alphalib.utils import logger
from alphalib.models import Stock

COUNTRY = "united states"
SYMBOL = "BAC"


class TestFundamental(unittest.TestCase):
    """Test out the fundamental indicator."""

    ma = MarketAnalysis(country=COUNTRY)
    fa = FundamentalAnalysis(country=COUNTRY, symbol=SYMBOL)

    countries: list[str]
    stocks: pd.DataFrame

    def setUp(self):
        logger.info("Setup")

    def tearDown(self):
        logger.info("Tear down")

    def test_get_countries(self):
        self.countries = MarketAnalysis.get_countries()
        self.assertGreater(len(self.countries), 0)
        logger.debug(self.countries)

    def test_get_stocks(self):
        """Get stocks for a country."""
        self.stocks = self.ma.get_stocks()
        self.assertGreater(len(self.stocks), 0)
        logger.debug(self.stocks.head(10))

    def test_get_stock_info(self):
        stock_info = self.fa.get_info()
        self.assertGreater(len(stock_info), 0)
        # records = stock_info.iloc[[0]].to_dict()
        records = stock_info.to_dict("records")
        print(records)
        # stock = Stock(**stock_info.to_dict())
        # print(stock)
        # for col in stock_info.columns:
        #     print(col)
        # logger.debug(stock_info.columns)
        # logger.debug(stock_info.T)

    def test_get_stocks_financials(self):
        financials = self.fa.get_financials()
        logger.info(type(financials))

    def test_save_analysis(self):
        self.ma.save()
