import unittest
import unittest.mock

import pandas as pd
from openpyxl import load_workbook

from alphalib.dataset import Dataset
from alphalib.utils import logger

COUNTRY = "united states"
SYMBOL = "BAC"


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

    def test_get_dataset(self):
        self.dataset.download()
