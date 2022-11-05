# https://github.com/derekbanas/Python4Finance/blob/main/Ultimate%20Calc%20Stats.ipynb
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf

from alphalib.analysis.ta import trend_ichimoku


def get_fill_color(label):
    if label >= 1:
        return "rgba(0,250,0,0.4)"
    else:
        return "rgba(250,0,0,0.4)"


def plot_ichimoku(symbol: str, period: str = "1y"):
    assert symbol

    stock = yf.Ticker(symbol)
    df = stock.history(period=period)
    (
        df["Conversion"],
        df["Baseline"],
        df["SpanA"],
        df["SpanB"],
        df["Lagging"],
    ) = trend_ichimoku(df["High"], df["Low"], df["Close"])

    candle = go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candlestick",
    )

    df1 = df.copy()
    pio.templates.default = "plotly_dark"
    fig = go.Figure()
    df["label"] = np.where(df["SpanA"] > df["SpanB"], 1, 0)
    df["group"] = df["label"].ne(df["label"].shift()).cumsum()

    df = df.groupby("group")

    dfs = []
    for _, data in df:
        dfs.append(data)

    for df in dfs:
        fig.add_traces(
            go.Scatter(x=df.index, y=df.SpanA, line=dict(color="rgba(0,0,0,0)"))
        )
        fig.add_traces(
            go.Scatter(
                x=df.index,
                y=df.SpanB,
                line=dict(color="rgba(0,0,0,0)"),
                fill="tonexty",
                fillcolor=get_fill_color(df["label"].iloc[0]),
            )
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

    fig.add_trace(candle)
    fig.add_trace(baseline)
    fig.add_trace(conversion)
    fig.add_trace(lagging)
    fig.add_trace(span_a)
    fig.add_trace(span_b)
    fig.update_layout(
        title_text=f"Ichimoku - {symbol.upper()}",
        height=1200,
        width=1800,
        showlegend=True,
    )

    fig.show()
