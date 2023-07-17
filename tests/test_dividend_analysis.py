from unittest import TestCase
from PIL.GifImagePlugin import getdata
import pandas as pd


from yahooquery import Ticker

from alphalib.data_sources.nasdaq import get_dividend_info, Nasdaq
from alphalib.analysis.dividend import dividend_analysis

# For testing
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
# pd.set_option("display.max_colwidth", None)


DIVIDEND_HISTORY_YEARS = 8


class TestDividendAnalysis(TestCase):
    symbol = "OXLC"

    def test_download_dividend_history(self):
        stock: Nasdaq = get_dividend_info(self.symbol)
        stock.dividend_history.to_excel(f"data/{self.symbol}.xlsx", index=False)

    def test_download_price_history(self):
        ticker = Ticker(self.symbol)
        ticker.session.close()

    def test_dividend_history_analysis(self):
        dividend_analysis(self.symbol)

    def test_news_sentiment_score(self):
        pass
