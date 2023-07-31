from unittest import TestCase
import pandas as pd


from alphalib.analysis.balance_sheet import balance_sheet_analysis

# For testing
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


class TestBalanceSheet(TestCase):
    symbol = "KEN"

    def test_balance_sheet_analysis(self):
        analysis = balance_sheet_analysis(self.symbol)
