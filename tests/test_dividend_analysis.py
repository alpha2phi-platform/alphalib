from unittest import TestCase
import pandas as pd


from alphalib.data_sources.nasdaq import get_dividend_info, Nasdaq
from alphalib.analysis.dividend import dividend_analysis

# For testing
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


DIVIDEND_HISTORY_YEARS = 8


class TestDividendAnalysis(TestCase):
    symbol = "EFC"

    def test_download_dividend_history(self):
        stock: Nasdaq = get_dividend_info(self.symbol)
        stock.dividend_history.to_excel(f"data/{self.symbol}.xlsx", index=False)

    def test_dividend_history_analysis(self):
        dividend_analysis(self.symbol)
