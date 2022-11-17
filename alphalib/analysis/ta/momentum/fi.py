import pandas as pd
import yfinance as yf


def calculate_fi(df, ndays):
    fi = pd.Series(df["Close"].diff(ndays) * df["Volume"], name="ForceIndex")
    df = df.join(fi)
    return df


def plot_fi(symbol: str, period: str = "1y"):
    assert symbol

    stock = yf.Ticker(symbol)
    df = stock.history(period=period)

    # Compute the Force Index for AAPL
    n = 1
    fi = calculate_fi(df, n)
    fi["ForceIndex"]
