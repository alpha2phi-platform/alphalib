import unittest
import unittest.mock

import pandas as pd

from alphalib.analysis.fa import (all_sources, nasdaq, seeking_alpha,
                                  yahoo_finance)
from alphalib.analysis.high_yield import recommend_stocks
from alphalib.analysis.sentiment import sentiment_analysis
from alphalib.analysis.ta.momentum.rsi import plot_rsi
from alphalib.analysis.ta.trend.ichimoku import plot_ichimoku
from alphalib.analysis.ta.volatility.atr import plot_atr
from alphalib.analysis.ta.volatility.bb import plot_bollinger_bands
from alphalib.analysis.technical import plot_technical
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
        analysis = nasdaq("gogl")
        print(analysis)

    def test_yahoo_finance(self):
        analysis = yahoo_finance("CLM")
        print(analysis.to_df().head().T)

    def test_high_yield(self):
        recommend_stocks(by="sector")

    def test_sentiment(self):
        df = sentiment_analysis("googl")
        past_3_months = month_from(-2)
        print(df[df["date"] >= past_3_months].head(1000))
        mean_score = df[df["date"] >= past_3_months]["compound"].mean()
        print(f"\n\nMean score - {mean_score}")

    def test_ta_bb(self):
        plot_bollinger_bands("googl")

    def test_ta_ichimoku(self):
        plot_ichimoku("googl")

    def test_ta_rsi(self):
        plot_rsi("googl")

    def test_ta_atr(self):
        plot_atr("googl")

    def test_ta(self):
        plot_technical("googl")
