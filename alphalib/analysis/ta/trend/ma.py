import pandas as pd


def SMA(data, ndays=50):
    """ "Simple moving average.
        data (pandas.DataFrame): A pandas data frame.
        ndays (int): Number of days.

    Returns:
        A pandas data frame.
    """
    SMA = pd.Series(data["Close"].rolling(ndays).mean(), name="SMA")
    data = data.join(SMA)
    return data


#
def EWMA(data, ndays):
    """Exponentially-weighted Moving Average.
        data (pandas.Dataframe): A pandas data frame.
        ndays (int): Number of days.

    Returns:
        A pandas data frame.
    """
    EMA = pd.Series(
        data["Close"].ewm(span=ndays, min_periods=ndays - 1).mean(),
        name="EWMA_" + str(ndays),
    )
    data = data.join(EMA)
    return data
