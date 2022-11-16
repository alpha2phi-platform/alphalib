import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf


def calculate_ewma(data, ndays):
    """Exponentially-weighted Moving Average.
        data (pandas.Dataframe): A pandas data frame.
        ndays (int): Number of days.

    Returns:
        A pandas data frame.
    """
    ema = pd.Series(
        data["Close"].ewm(span=ndays, min_periods=ndays - 1).mean(), name="EWMA"
    )
    data = data.join(ema)
    return data


def plot_ewma(symbol: str, period: str = "1y", ndays=200):
    assert symbol

    stock = yf.Ticker(symbol)
    df = stock.history(period=period)

    ewma = calculate_ewma(df, ndays)
    ewma = ewma.dropna()
    ewma = ewma["EWMA"]

    pio.templates.default = "plotly_dark"
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df.index, y=df["Close"], name="Price", line_color="#636EFA")
    )
    fig.add_trace(go.Scatter(x=ewma.index, y=ewma, name="EWMA", line_color="#FECB52"))

    fig.update_xaxes(title="Date", rangeslider_visible=True)
    fig.update_yaxes(title="Price")
    fig.update_layout(
        title_text=f"Trend Indicator - Exponentially-weighted Moving Average for {symbol.upper()}",
        height=1200,
        width=1800,
        showlegend=True,
    )
    fig.show()
