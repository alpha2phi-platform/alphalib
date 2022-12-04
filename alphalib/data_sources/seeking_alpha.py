from dataclasses import dataclass
from datetime import datetime

import pandas as pd
from requests import Response

from alphalib.data_sources import invoke_api
from alphalib.utils.convertutils import TypeConverter

SEEKING_ALPHA_DIVIDEND_HISTORY_API_ENDPOINT = "https://seekingalpha.com/api/v3/symbols/{0}/dividend_history?group_by=quarterly&sort=-date"

SEEKING_ALPHA_ESTIMATED_EARNING_ANNOUNCES_API_ENDPOINT = (
    "https://seekingalpha.com/api/v3/symbol_data/estimated_earning_announces?slug={0}"
)


@dataclass
class SeekingAlpha(TypeConverter):
    symbol: str = ""
    seeking_alpha_url: str = ""
    estimated_earning_date: datetime = datetime.min
    dividend_history: pd.DataFrame = pd.DataFrame()


def process_dividend_history(
    r: Response, symbol: str, api_endpoint: str
) -> SeekingAlpha:
    sa = SeekingAlpha()
    sa.symbol = symbol
    sa.seeking_alpha_url = api_endpoint

    results = []
    json: dict = r.json()
    for row in json["data"]:
        results.append(row["attributes"])
    if len(results) > 0:
        sa.dividend_history = pd.json_normalize(results)

    return sa


def process_estimated_earning_dt(r: Response, symbol: str, _: str):
    json: dict = r.json()
    if json[f"{symbol.upper()}"]:
        return json[f"{symbol.upper()}"]["release_date"]

    return datetime.min


def get_stock_info(symbol: str) -> SeekingAlpha:
    assert symbol

    # Dividend history
    api_endpoint = SEEKING_ALPHA_DIVIDEND_HISTORY_API_ENDPOINT.format(symbol.upper())
    sa = invoke_api(symbol, api_endpoint, process_dividend_history)

    api_endpoint = SEEKING_ALPHA_ESTIMATED_EARNING_ANNOUNCES_API_ENDPOINT.format(
        symbol.upper()
    )
    sa.estimated_earning_date = datetime.strptime(
        invoke_api(symbol, api_endpoint, process_estimated_earning_dt),
        "%Y-%m-%dT00:00:00.000Z",
    )
    return sa
