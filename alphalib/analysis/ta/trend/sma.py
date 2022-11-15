import matplotlib.pyplot as plt
import pandas as pd
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


def plot_sma(symbol: str, period: str = "1y"):
    assert symbol

    stock = yf.Ticker(symbol)
    df = stock.history(period=period)

    # Compute the 50-day SMA
    n = 50
    sma = calculate_sma(df, n)
    sma = sma.dropna()
    sma = sma["SMA"]

    # Plotting the Google stock Price Series chart and Moving Averages below
    plt.figure(figsize=(10, 7))

    # Set the title and axis labels
    plt.title("Moving Average")
    plt.xlabel("Date")
    plt.ylabel("Price")

    # Plot close price and moving averages
    plt.plot(df["Close"], lw=1, label="Close Price")
    plt.plot(sma, "g", lw=1, label="50-day SMA")
    # plt.plot(ewma, "r", lw=1, label="200-day EMA")

    # Add a legend to the axis
    plt.legend()

    plt.show()
