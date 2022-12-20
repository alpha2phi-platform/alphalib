from dataclasses import dataclass
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
from requests import Response
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from alphalib.data_sources import invoke_api
from alphalib.utils.convertutils import TypeConverter, strip, to_date, to_float
from alphalib.utils.httputils import get_driver, get_tag_value
from alphalib.utils.logger import logger

NASDAQ_DIVIDEND_HISTORY_URL = (
    "https://www.nasdaq.com/market-activity/stocks/{0}/dividend-history"
)

NASAQ_DIVIDEND_HISTORY_API_ENDPOINT = (
    "https://api.nasdaq.com/api/quote/{0}/dividends?assetclass=stocks"
)


@dataclass
class Nasdaq(TypeConverter):
    symbol: str = ""
    ex_dividend_date: datetime = datetime.min
    dividend_yield_pct: float = 0
    annual_dividend: float = 0
    pe_ratio: float = 0
    dividend_history: pd.DataFrame = pd.DataFrame()
    nasdaq_url: str = ""


def process_stock_info(r: Response, symbol: str, api_endpoint: str) -> Nasdaq:
    nasdaq = Nasdaq()
    nasdaq.symbol = symbol
    nasdaq.nasdaq_url = api_endpoint
    results = []
    json: dict = r.json()
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


def get_stock_info(symbol: str) -> Nasdaq:
    assert symbol

    api_endpoint = NASAQ_DIVIDEND_HISTORY_API_ENDPOINT.format(symbol.upper())
    nasdaq = invoke_api(symbol, api_endpoint, process_stock_info)
    return nasdaq
