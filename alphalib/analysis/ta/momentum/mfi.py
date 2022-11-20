import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf
from plotly.subplots import make_subplots


def gain(x):
    return ((x > 0) * x).sum()


def loss(x):
    return ((x < 0) * x).sum()


def calculate_mfi(high, low, close, volume, n=14):
    typical_price = (high + low + close) / 3
    money_flow = typical_price * volume
    mf_sign = np.where(typical_price > typical_price.shift(1), 1, -1)
    signed_mf = money_flow * mf_sign
    mf_avg_gain = signed_mf.rolling(n).apply(gain, raw=True)
    mf_avg_loss = signed_mf.rolling(n).apply(loss, raw=True)
    return (100 - (100 / (1 + (mf_avg_gain / abs(mf_avg_loss))))).to_numpy()


def plot_mfi(symbol: str, period: str = "1y"):
    assert symbol

    stock = yf.Ticker(symbol)
    df = stock.history(period=period)

    df["MFI"] = calculate_mfi(df["High"], df["Low"], df["Close"], df["Volume"], 14)

    pio.templates.default = "plotly_dark"
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("Price", "MFI"),
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
            y=df["MFI"],
            name="MFI",
            line_color="rgb(204,0,0)",
        ),
        row=2,
        col=1,
    )

    fig.update_layout(title_text=f"Volume Indicator - MFI for {symbol.upper()}")
    fig.update_xaxes(title="Date", rangeslider_visible=True, row=2, col=1)
    fig.update_yaxes(title="Price", row=1, col=1)
    fig.update_yaxes(title="MFI", row=2, col=1)
    fig.show()
    # Plotting the Price Series chart and the MFI below
    # fig = plt.figure(figsize=(10, 7))

    # # Define position of 1st subplot
    # ax = fig.add_subplot(2, 1, 1)

    # # Set the title and axis labels
    # plt.title("Apple Price Chart")
    # plt.xlabel("Date")
    # plt.ylabel("Close Price")

    # plt.plot(df["Close"], label="Close price")

    # # Add a legend to the axis
    # plt.legend()

    # # Define position of 2nd subplot
    # bx = fig.add_subplot(2, 1, 2)

    # # Set the title and axis labels
    # plt.title("Money flow index")
    # plt.xlabel("Date")
    # plt.ylabel("MFI values")

    # plt.plot(df["MFI"], "m", label="MFI")

    # # Add a legend to the axis
    # plt.legend()

    # plt.tight_layout()
    # plt.show()
