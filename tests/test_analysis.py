import unittest
import unittest.mock

import pandas as pd

from alphalib.analysis import all_sources, nasdaq, seeking_alpha, yahoo_finance
from alphalib.analysis.dividend_yield import recommend_stocks
from alphalib.analysis.sentiment import analyze_sentiment
from alphalib.utils.dateutils import month_from

# For testing
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
# pd.set_option("display.max_colwidth", None)


class TestAnalysis(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_stock_analysis(self):
        stock_analysis = all_sources("orc")
        print(stock_analysis)

    def test_seeking_alpha(self):
        analysis = seeking_alpha("MFA")
        print(analysis)

    def test_nasdaq(self):
        analysis = nasdaq("PBR")
        print(analysis)

    def test_yahoo_finance(self):
        analysis = yahoo_finance("PBR")
        print(analysis.to_df().head().T)

    def test_high_yield(self):
        recommend_stocks(by="sector")

    def test_sentiment(self):
        df = analyze_sentiment("orc")
        past_3_months = month_from(-2)
        print(past_3_months)
        print(df[df["date"] >= past_3_months].head(1000))

        mean_score = df[df["date"] >= past_3_months]["compound"].mean()
        print(f"\n\nMean score - {mean_score}")
