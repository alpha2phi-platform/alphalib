import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf
from plotly.subplots import make_subplots

from alphalib.analysis.ta.momentum.rsi import calculate_rsi
from alphalib.analysis.ta.trend.ichimoku import calculate_ichimoku
from alphalib.analysis.ta.volatility.atr import calculate_atr


def plot_technical(symbol: str, period: str = "1y"):
    assert symbol

    df = yf.download(symbol, period=period)
    df["RSI"], rsi_buyers, rsi_sellers = calculate_rsi(df["Close"])
    df["ATR"] = calculate_atr(df["High"], df["Low"], df["Close"])
    df["RSI_ATR"] = df["RSI"] / df["ATR"]
    df["RSI_ATR"], rsi_atr_buyers, rsi_atr_sellers = calculate_rsi(df["RSI_ATR"])

    pio.templates.default = "plotly_dark"
    fig = make_subplots(
        rows=3,
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
            x=rsi_buyers.index,
            y=rsi_buyers["Close"],
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
            x=rsi_sellers.index,
            y=rsi_sellers["Close"],
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

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["RSI_ATR"],
            name="RSI ATR",
            line_color="rgb(218,112,214)",
        ),
        row=3,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=rsi_atr_buyers.index,
            y=rsi_atr_buyers["Close"],
            name="Buyers",
            mode="markers",
            marker=dict(
                color="#00CC96",
                size=10,
            ),
        ),
        row=3,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=rsi_atr_sellers.index,
            y=rsi_atr_sellers["Close"],
            name="Sellers",
            mode="markers",
            marker=dict(
                color="#EF553B",
                size=10,
            ),
        ),
        row=3,
        col=1,
    )

    fig.update_layout(title_text=f"Technical Analysis - {symbol.upper()}")
    fig.update_xaxes(title="Date", rangeslider_visible=True, row=3, col=1)
    fig.update_yaxes(title="Price", row=1, col=1)
    fig.update_yaxes(title="RSI", row=2, col=1)
    fig.update_yaxes(title="RSI ATR", row=3, col=1)
    fig.show()
