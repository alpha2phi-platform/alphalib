import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf
from plotly.subplots import make_subplots

from alphalib.analysis.ta.momentum.rsi import calculate_rsi
from alphalib.analysis.ta.trend.ichimoku import calculate_ichimoku
from alphalib.analysis.ta.volatility.atr import calculate_atr
from alphalib.analysis.ta.volatility.bb import calculate_bb


def plot_close(df, fig, row=1, col=1):
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["Close"],
            name="Price",
            line_color="rgb(0,204,0)",
        ),
        row=row,
        col=col,
    )
    fig.update_yaxes(title="Price", row=row, col=col)


def plot_rsi(df, fig, row=1, col=1):
    df["RSI"], rsi_buyers, rsi_sellers = calculate_rsi(df["Close"])
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["RSI"],
            name="RSI",
            line_color="rgb(204,0,0)",
        ),
        row=row,
        col=col,
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
        row=row,
        col=col,
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
        row=row,
        col=col,
    )
    fig.update_yaxes(title="RSI", row=row, col=col)


def plot_rsi_atr(df, fig, row=1, col=1):
    df["ATR"] = calculate_atr(df["High"], df["Low"], df["Close"])
    df["RSI_ATR"] = df["RSI"] / df["ATR"]
    df["RSI_ATR"], rsi_atr_buyers, rsi_atr_sellers = calculate_rsi(df["RSI_ATR"])

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df["RSI_ATR"],
            name="RSI ATR",
            line_color="rgb(218,112,214)",
        ),
        row=row,
        col=col,
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
        row=row,
        col=col,
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
        row=row,
        col=col,
    )
    fig.update_yaxes(title="RSI ATR", row=row, col=col)


def get_fill_color(label):
    if label >= 1:
        return "rgba(0,250,0,0.4)"
    else:
        return "rgba(250,0,0,0.4)"


def plot_ichimoku(df, fig, row=1, col=1):
    (
        df["Conversion"],
        df["Baseline"],
        df["SpanA"],
        df["SpanB"],
        df["Lagging"],
    ) = calculate_ichimoku(df["High"], df["Low"], df["Close"])

    candle = go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candlestick",
    )

    df1 = df.copy()

    df["label"] = np.where(df["SpanA"] > df["SpanB"], 1, 0)
    df["group"] = df["label"].ne(df["label"].shift()).cumsum()

    df = df.groupby("group")

    dfs = []
    for _, data in df:
        dfs.append(data)

    for df in dfs:
        fig.add_trace(
            go.Scatter(x=df.index, y=df.SpanA, line=dict(color="rgba(0,0,0,0)")),
            row=row,
            col=col,
        )
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df.SpanB,
                line=dict(color="rgba(0,0,0,0)"),
                fill="tonexty",
                fillcolor=get_fill_color(df["label"].iloc[0]),
            ),
            row=row,
            col=col,
        )

    baseline = go.Scatter(
        x=df1.index,
        y=df1["Baseline"],
        line=dict(color="pink", width=2),
        name="Baseline",
    )

    conversion = go.Scatter(
        x=df1.index,
        y=df1["Conversion"],
        line=dict(color="black", width=1),
        name="Conversion",
    )

    lagging = go.Scatter(
        x=df1.index,
        y=df1["Lagging"],
        line=dict(color="purple", width=2),
        name="Lagging",
    )

    span_a = go.Scatter(
        x=df1.index,
        y=df1["SpanA"],
        line=dict(color="green", width=2, dash="dot"),
        name="Span A",
    )

    span_b = go.Scatter(
        x=df1.index,
        y=df1["SpanB"],
        line=dict(color="red", width=1, dash="dot"),
        name="Span B",
    )

    fig.add_trace(candle, row=row, col=col)
    fig.add_trace(baseline, row=row, col=col)
    fig.add_trace(conversion, row=row, col=col)
    fig.add_trace(lagging, row=row, col=col)
    fig.add_trace(span_a, row=row, col=col)
    fig.add_trace(span_b, row=row, col=col)

    fig.update_yaxes(title="Ichimoku", row=row, col=col)


def plot_bollinger_bands(df, fig, row=1, col=1):
    df_close = df[["Close"]]
    sma, lower_band, upper_band, buyers, sellers = calculate_bb(df_close)

    fig.add_trace(
        go.Scatter(
            x=lower_band.index,
            y=lower_band["Lower"],
            name="Lower Band",
            line_color="rgba(173,204,255,0.2)",
        ),
        row=row,
        col=col,
    )
    fig.add_trace(
        go.Scatter(
            x=upper_band.index,
            y=upper_band["Upper"],
            name="Upper Band",
            fill="tonexty",
            fillcolor="rgba(173,204,255,0.2)",
            line_color="rgba(173,204,255,0.2)",
        ),
        row=row,
        col=col,
    )
    fig.add_trace(
        go.Scatter(
            x=df_close.index, y=df_close["Close"], name="Price", line_color="#636EFA"
        ),
        row=row,
        col=col,
    )
    fig.add_trace(
        go.Scatter(x=sma.index, y=sma["Close"], name="SMA", line_color="#FECB52"),
        row=row,
        col=col,
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
        row=row,
        col=col,
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
        row=row,
        col=col,
    )
    fig.update_yaxes(title="Bollinger Bands", row=row, col=col)


def plot_technical(symbol: str, period: str = "1y"):
    assert symbol

    df = yf.download(symbol, period=period)
    pio.templates.default = "plotly_dark"

    fig = make_subplots(
        rows=5,
        cols=1,
        row_heights=[0.15, 0.15, 0.15, 0.2, 0.45],
        shared_xaxes=True,
        subplot_titles=(
            "Price",
            "Momentum - RSI",
            "Volatility - RSI ATR",
            "Volatility - Bollinger Bands",
            "Trend - Ichimoku",
        ),
    )

    plot_close(df, fig, row=1)
    plot_rsi(df, fig, row=2)
    plot_rsi_atr(df, fig, row=3)
    plot_bollinger_bands(df, fig, row=4)
    plot_ichimoku(df, fig, row=5)

    fig.update_layout(
        title_text=f"Technical Analysis - {symbol.upper()}",
        showlegend=True,
        height=2400,
        width=1800,
    )
    fig.update_xaxes(title="Date", rangeslider_visible=True, row=5, col=1)
    fig.show()
