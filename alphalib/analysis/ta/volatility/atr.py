import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf
from plotly.subplots import make_subplots


def calculate_atr(high, low, close, n=14):
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


def plot_atr(symbol: str, period: str = "1y"):
    assert symbol

    df = yf.download(symbol, period=period)
    df["ATR"] = calculate_atr(df["High"], df["Low"], df["Close"])

    pio.templates.default = "plotly_dark"
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("Price", "ATR"),
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            name="Price",
            line_color="rgb(0,204,0)",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["ATR"],
            name="ATR",
            line_color="rgb(204,0,0)",
        ),
        row=2,
        col=1,
    )

    fig.update_layout(title_text=f"Volatility Indicator - ATR for {symbol.upper()}")
    fig.update_xaxes(title="Date", rangeslider_visible=True, row=2, col=1)
    fig.update_yaxes(title="Price", row=1, col=1)
    fig.update_yaxes(title="ATR", row=2, col=1)
    fig.show()
