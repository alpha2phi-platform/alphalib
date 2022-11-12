import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf
from plotly.subplots import make_subplots


def calculate_rsi(close, periods=14, upper=70, lower=30):

    close_delta = close.diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))

    buyers = rsi[rsi <= lower]
    sellers = rsi[rsi >= upper]

    return rsi, pd.DataFrame({"Close": buyers}), pd.DataFrame({"Close": sellers})


def plot_rsi(symbol: str, period: str = "1y"):
    assert symbol

    df = yf.download(symbol, period=period)
    df["RSI"], buyers, sellers = calculate_rsi(df["Close"])

    pio.templates.default = "plotly_dark"
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("Price", "RSI"),
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
            y=df["RSI"],
            name="RSI",
            line_color="rgb(204,0,0)",
        ),
        row=2,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=buyers.index,
            y=buyers["Close"],
            name="Buyers",
            mode="markers",
            marker=dict(
                color="#00CC96",
                size=10,
            ),
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=sellers.index,
            y=sellers["Close"],
            name="Sellers",
            mode="markers",
            marker=dict(
                color="#EF553B",
                size=10,
            ),
        ),
        row=2,
        col=1,
    )

    fig.update_layout(title_text=f"Momentum Indicator - RSI for {symbol.upper()}")
    fig.update_xaxes(title="Date", rangeslider_visible=True, row=2, col=1)
    fig.update_yaxes(title="Price", row=1, col=1)
    fig.update_yaxes(title="RSI", row=2, col=1)
    fig.show()
