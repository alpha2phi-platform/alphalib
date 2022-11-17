import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


def calculate_emv(df, ndays):
    dm = ((df["High"] + df["Low"]) / 2) - (
        (df["High"].shift(1) + df["Low"].shift(1)) / 2
    )
    br = (df["Volume"] / 100000000) / ((df["High"] - df["Low"]))
    emv = dm / br
    emv_ma = pd.Series(emv.rolling(ndays).mean(), name="EMV")
    df = df.join(emv_ma)
    return df


def plot_emv(symbol: str, period: str = "1y", ndays=14):
    assert symbol

    stock = yf.Ticker(symbol)
    df = stock.history(period=period)

    # Compute the 14-day Ease of Movement for AAPL
    emv = calculate_emv(df, ndays)
    emv = emv["EMV"]

    # Plotting the Price Series chart and the Ease Of Movement below
    fig = plt.figure(figsize=(10, 7))

    # Define position of 1st subplot
    ax = fig.add_subplot(2, 1, 1)

    # Set the title and axis labels
    plt.title("AAPL Price Chart")
    plt.xlabel("Date")
    plt.ylabel("Close Price")

    # Plot the close price of the Apple
    plt.plot(df["Close"], label="Close price")

    # Add a legend to the axis
    plt.legend()

    # Define position of 2nd subplot
    bx = fig.add_subplot(2, 1, 2)

    # Set the title and axis labels
    plt.title("Ease Of Movement Chart")
    plt.xlabel("Date")
    plt.ylabel("EMV values")

    # Plot the ease of movement
    plt.plot(emv, "m", label="EMV(14)")

    # Add a legend to the axis
    plt.legend()

    plt.tight_layout()
    plt.show()
