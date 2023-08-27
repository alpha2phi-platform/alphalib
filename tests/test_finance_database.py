import unittest
from alphalib.dataset.finance_database import prepare_stock_dataset


class TestFinanceDatabase(unittest.TestCase):
    def test_prepare_dadtabase(self):
        df = prepare_stock_dataset()
        print(len(df))
        print(df.tail(10))
