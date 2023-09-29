from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from requests import Response

from alphalib.data_sources import invoke_api
from alphalib.utils.convertutils import TypeConverter

NASAQ_DIVIDEND_HISTORY_API_ENDPOINT = (
    "https://api.nasdaq.com/api/quote/{0}/dividends?assetclass=stocks"
)


@dataclass(kw_only=True)
class Nasdaq(TypeConverter):
    symbol: str = ""
    ex_dividend_date: datetime = datetime.min
    dividend_yield_pct: float = 0
    annual_dividend: float = 0
    pe_ratio: float = 0
    dividend_history: pd.DataFrame = pd.DataFrame()
    nasdaq_url: str = ""


def process_dividend_info(r: Response, symbol: str, api_endpoint: str) -> Nasdaq:
    nasdaq = Nasdaq()
    nasdaq.symbol = symbol
    nasdaq.nasdaq_url = api_endpoint
    results = []
    json: dict = r.json()
    if json["data"]:
        nasdaq.ex_dividend_date = json["data"]["exDividendDate"]
        nasdaq.dividend_yield_pct = json["data"]["yield"]
        nasdaq.pe_ratio = json["data"]["payoutRatio"]
        nasdaq.annual_dividend = json["data"]["annualizedDividend"]
        dividends = json["data"]["dividends"]["rows"]
        if dividends:
            for row in dividends:
                results.append(row)
        if len(results) > 0:
            nasdaq.dividend_history = pd.json_normalize(results)
    return nasdaq


def get_dividend_info(symbol: str) -> Nasdaq:
    assert symbol

    api_endpoint = NASAQ_DIVIDEND_HISTORY_API_ENDPOINT.format(symbol.upper())
    nasdaq = invoke_api(symbol, api_endpoint, process_dividend_info)
    return nasdaq
