import pandas as pd


def calculate_ewma(data, ndays):
    """Exponentially-weighted Moving Average.
        data (pandas.Dataframe): A pandas data frame.
        ndays (int): Number of days.

    Returns:
        A pandas data frame.
    """
    ema = pd.Series(
        data["Close"].ewm(span=ndays, min_periods=ndays - 1).mean(),
        name="EWMA_" + str(ndays),
    )
    data = data.join(ema)
    return data


def plot_ewma(symbol: str, period: str = "1y"):
    assert symbol

    # Compute the 200-day EWMA
    ew = 200
    ewma = calculate_ewma(data, ew)
    ewma = ewma.dropna()
    ewma = ewma["EWMA_200"]

    # Plotting the Google stock Price Series chart and Moving Averages below
    plt.figure(figsize=(10, 7))

    # Set the title and axis labels
    plt.title("Moving Average")
    plt.xlabel("Date")
    plt.ylabel("Price")

    # Plot close price and moving averages
    plt.plot(data["Close"], lw=1, label="Close Price")
    plt.plot(sma, "g", lw=1, label="50-day SMA")
    plt.plot(ewma, "r", lw=1, label="200-day EMA")

    # Add a legend to the axis
    plt.legend()

    plt.show()
