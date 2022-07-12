import pandas as pd
import yfinance as yf


def get_stock_info(_, symbol):
    return pd.DataFrame([yf.Ticker(symbol).info])
