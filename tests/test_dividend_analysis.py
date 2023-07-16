from unittest import TestCase
import pandas as pd

from alphalib.utils.dateutils import years_from_now

from yahooquery import Ticker


# For testing
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
# pd.set_option("display.max_colwidth", None)


DIVIDEND_HISTORY_YEARS = 8


class TestDividendAnalysis(TestCase):
    def test_download_dividend_history(self):
        symbol = "OXLC"
        ticker = Ticker(symbol)
        df_div_history = ticker.dividend_history(
            start=years_from_now(DIVIDEND_HISTORY_YEARS)
        )
        print(df_div_history)

        ticker.session.close()

    def test_download_price_history(self):
        symbol = "OXLC"
        ticker = Ticker(symbol)
        ticker.session.close()

    def test_dividend_history_analysis(self):
        pass

    def test_news_sentiment_score(self):
        print("testing")
