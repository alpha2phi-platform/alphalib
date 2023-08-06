import unittest
import unittest.mock

import pandas as pd

from alphalib.analysis.recommender import (
    recommend_stocks_from_dataset,
    recommend_stocks_from_watchlist,
)
from alphalib.analysis.sentiment import finwiz_score, yahoo_finance_score
from alphalib.analysis.ta.momentum.mfi import plot_mfi
from alphalib.analysis.ta.momentum.rsi import plot_rsi
from alphalib.analysis.ta.trend.ewma import plot_ewma
from alphalib.analysis.ta.trend.ichimoku import plot_ichimoku
from alphalib.analysis.ta.trend.sma import plot_sma
from alphalib.analysis.ta.volatility.atr import plot_atr
from alphalib.analysis.ta.volatility.bb import plot_bollinger_bands
from alphalib.analysis.ta.volume.emv import plot_emv, plot_emv2
from alphalib.analysis.technical import plot_technical
from alphalib.utils.dateutils import month_from
from alphalib.analysis.piotroski import get_piotroski_score

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

    def test_recommend_stocks_watchlist(self):
        print(recommend_stocks_from_watchlist())

    def test_recommend_stocks_dataset(self):
        print(recommend_stocks_from_dataset())

    def test_sentiment_finwiz_score(self):
        df = finwiz_score("afsia")
        past_x_months = month_from(-4)
        print(df[df["date"] >= past_x_months.date()].head(1000))
        mean_score = df[df["date"] >= past_x_months.date()]["compound"].mean()
        print(f"\n\nMean score - {mean_score}")

    def test_sentiment_yahoo_finance_score(self):
        # TODO:
        df = yahoo_finance_score("sblk")

    def test_piostroski_score(self):
        print(get_piotroski_score("oxlc"))

    def test_ta_bb(self):
        plot_bollinger_bands("googl")

    def test_ta_ichimoku(self):
        plot_ichimoku("ken")

    def test_ta_rsi(self):
        plot_rsi("googl")

    def test_ta_atr(self):
        plot_atr("googl")

    def test_ta_sma(self):
        plot_sma("googl")

    def test_ta_ewma(self):
        plot_ewma("googl")

    def test_ta_mfi(self):
        plot_mfi("googl")

    def test_ta_emv(self):
        plot_emv("googl")

    def test_ta_emv2(self):
        plot_emv2("googl")

    def test_ta(self):
        plot_technical("googl")
