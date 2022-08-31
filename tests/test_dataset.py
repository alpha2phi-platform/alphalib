import unittest
import unittest.mock

import pandas as pd
import yfinance as yf

from alphalib.dataset import Dataset
from alphalib.utils import logger

COUNTRY = "united states"
SYMBOL = "BA"


# For testing
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
# pd.set_option("display.max_colwidth", None)


class TestDataset(unittest.TestCase):
    """Test out the fundamental indicator."""

    dataset = Dataset(country=COUNTRY)

    # All stock countries
    countries: list[str]

    # Stocks for a country
    stocks: pd.DataFrame

    def setUp(self):
        self.countries = Dataset.get_countries()
        self.stocks = self.dataset.get_stocks()

    def tearDown(self):
        logger.info("Tear down")

    def test_get_ticker(self):
        ticker = yf.Ticker(SYMBOL)
        stock_info = pd.DataFrame([ticker.info])
        print(stock_info.T)

    def test_list_diff(self):
        a = ["a", "b", "c", "e"]
        b = ["a", "b", "c", "d"]
        c = list(set(b) - set(a))
        d = list(set(b).symmetric_difference(set(a)))
        print(c)
        print(d)

    def test_get_dataset(self):
        self.dataset.download(continue_from_last_download=True)
