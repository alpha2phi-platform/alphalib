from datetime import datetime, timedelta
from unittest import TestCase

import numpy as np
import pandas as pd
from alphalib.analysis import get_historical_prices
from alphalib.analysis.dividend import dividend_analysis
from alphalib.analysis.ml.time_series import predict_time_series
from alphalib.data_sources.nasdaq import Nasdaq, get_dividend_info

# For testing
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


class TestStockAnalysis(TestCase):
    symbol = "abbv"

    def test_download_dividend_history(self):
        stock: Nasdaq = get_dividend_info(self.symbol)
        stock.dividend_history.to_excel(f"data/{self.symbol}.xlsx", index=False)

    def test_dividend_history_analysis(self):
        analysis = dividend_analysis(self.symbol)
        print(analysis)
        print(analysis.target_buy_price)

    def test_dividend_analysis(self):
        # symbols = ["amzn", "goog"]
        # new_target_prices = [100, 200]
        # df = pd.DataFrame.from_dict(
        #     {"symbol": symbols, "target_buy_price": new_target_prices}
        # )
        # print(df.head())

        stocks = [
            {"symbol": "ABBV", "target_buy_price": 132.51},
            {"symbol": "GOGL", "target_buy_price": 6.9},
            {"symbol": "ORC", "target_buy_price": 9.22},
        ]
        df = pd.DataFrame(stocks)
        print(df.head())

        new_stocks = [
            {"symbol": "ABBV", "target_buy_price": 1},
            {"symbol": "GOGL", "target_buy_price": -1},
            {"symbol": "ORC", "target_buy_price": 100},
        ]
        df_new = pd.DataFrame(new_stocks)
        print(df_new.head())

        df["target_buy_price"] = np.where(
            df_new["target_buy_price"] > 0,
            df_new["target_buy_price"],
            df["target_buy_price"],
        )
        print(df.head())

    def test_get_historical_prices(self):
        df_prices = get_historical_prices(
            self.symbol, datetime.now() - timedelta(days=365 * 3), datetime.now()
        )
        df_prices["date"] = df_prices["date"].dt.date
        df_prices.to_excel(f"data/{self.symbol}_historical_prices.xlsx", index=False)
        print(df_prices.tail(50))

    def test_time_seris_analysis(self):
        df_prices, _ = predict_time_series(self.symbol)
        print(df_prices[["ds", "trend", "yhat", "yhat_lower", "yhat_upper"]].tail(50))
