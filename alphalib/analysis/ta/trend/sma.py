import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf


def calculate_sma(data, ndays=50):
    """ "Simple moving average.
        data (pandas.DataFrame): A pandas data frame.
        ndays (int): Number of days.

    Returns:
        A pandas data frame.
    """
    sma = pd.Series(data["Close"].rolling(ndays).mean(), name="SMA")
    data = data.join(sma)
    return data


def plot_sma(symbol: str, period: str = "1y", ndays=50):
    assert symbol

    stock = yf.Ticker(symbol)
    df = stock.history(period=period)

    # Compute the 50-day SMA
    sma = calculate_sma(df, ndays)
    sma = sma.dropna()
    sma = sma["SMA"]

    pio.templates.default = "plotly_dark"
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(x=df.index, y=df["Close"], name="Price", line_color="#636EFA")
    )
    fig.add_trace(go.Scatter(x=sma.index, y=sma, name="SMA", line_color="#FECB52"))

    fig.update_xaxes(title="Date", rangeslider_visible=True)
    fig.update_yaxes(title="Price")
    fig.update_layout(
        title_text=f"Trend Indicator - Simple Moving Average for {symbol.upper()}",
        height=1200,
        width=1800,
        showlegend=True,
    )
    fig.show()
