import pandas as pd
import yfinance as yf
from yfinance import Ticker


def get_stock(symbol) -> Ticker:
    return yf.Ticker(symbol)
