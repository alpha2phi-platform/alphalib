import matplotlib.pyplot as plt
import yfinance as yf
import plotly.graph_objects as go
import plotly.io as pio


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
