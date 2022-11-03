import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf
from plotly.subplots import make_subplots


# Returns RSI values
def rsi(close, periods=14):

    close_delta = close.diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    return rsi


# Returns ATR values
def atr(high, low, close, n=14):
    tr = np.amax(
        np.vstack(
            (
                (high - low).to_numpy(),
                (abs(high - close)).to_numpy(),
                (abs(low - close)).to_numpy(),
            )
        ).T,
        axis=1,
    )
    return pd.Series(tr).rolling(n).mean().to_numpy()


def plot_rsi(symbol: str, period: str = "1y"):
    # Retrieve the Apple Inc. data from Yahoo finance
    data = yf.download(symbol, period=period)

    # Call RSI function from the talib library to calculate RSI
    data["RSI"] = rsi(data["Close"])

    # Plotting the Price Series chart and the RSI below
    fig = plt.figure(figsize=(10, 7))

    # Define position of 1st subplot
    ax = fig.add_subplot(2, 1, 1)

    # Set the title and axis labels
    plt.title(f"RSI for {symbol}")
    plt.xlabel("Date")
    plt.ylabel("Close Price")

    plt.plot(data["Close"], label="Close price")

    # Add a legend to the axis
    plt.legend()

    # Define position of 2nd subplot
    bx = fig.add_subplot(2, 1, 2)

    # Set the title and axis labels
    plt.title("Relative Strength Index")
    plt.xlabel("Date")
    plt.ylabel("RSI values")

    plt.plot(data["RSI"], "m", label="RSI")

    # Add a legend to the axis
    plt.legend()

    plt.tight_layout()
    plt.show()


def plot_rsi2(symbol: str, period: str = "1y"):
    data = yf.download(symbol, period=period)
    data["RSI"] = rsi(data["Close"])

    pio.templates.default = "plotly_dark"
    fig = make_subplots(rows=2, cols=1)

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            name=f"Close Price - {symbol}",
            line_color="rgb(0,204,0)",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["RSI"],
            name=f"RSI - {symbol}",
            line_color="rgb(0,0,204)",
        ),
        row=2,
        col=1,
    )
    fig.update_xaxes(title="Date", rangeslider_visible=False, row=1, col=1)
    fig.update_xaxes(title="Date", rangeslider_visible=True, row=2, col=1)
    fig.update_yaxes(title="Price", row=1, col=1)
    fig.update_yaxes(title="RSI", row=2, col=1)
    fig.show()
