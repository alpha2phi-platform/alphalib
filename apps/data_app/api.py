# Imports
import pandas as pd
import requests


# API_KEY = "YOUR_API_KEY_HERE"


def get_screener_data(
    marketcapmorethan=1000000000,
    betamorethan=1,
    volmorethan=10000,
    sector="Technology",
    exchange="NASDAQ",
    dividendmorethan=0,
    limit=100,
    api_key: str = "",
):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    :param api_key: int
    :param limit:
    :param dividendmorethan:
    :param exchange:
    :param sector:
    :param volmorethan:
    :param marketcapmorethan:
    :param betamorethan:

    Returns
    -------
    dict
    """
    params = {
        "marketCapMoreThan": "{}".format(marketcapmorethan),
        "betaMoreThan": "{}".format(betamorethan),
        "volMoreThan": "{}".format(volmorethan),
        "sector": "{}".format(sector),
        "exchange": "{}".format(exchange),
        "dividendMoreThan": "{}".format(dividendmorethan),
        "limit": "{}".format(limit),
        "apikey": "{}".format(api_key),
    }  # Question: Is there a better way to write this? Is it possible to use format() just once?

    api_url = "https://financialmodelingprep.com/api/v3/stock-screener"

    response = requests.get(api_url, params=params)
    data = response.json()
    df = pd.DataFrame(data)
    return df  # Change this!
