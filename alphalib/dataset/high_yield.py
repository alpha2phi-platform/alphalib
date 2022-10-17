from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from selenium.webdriver.common.by import By

from alphalib.utils.convertutils import TypeConverter, strip, to_date, to_float
from alphalib.utils.httputils import (DEFAULT_HTTP_RETRY, DEFAULT_HTTP_TIMEOUT,
                                      http_headers, web_driver)

URL = "https://finance.yahoo.com/u/yahoo-finance/watchlists/high-yield-dividend-stocks/"


@dataclass
class HighYield(TypeConverter):
    symbol: str = ""
    company_name: str = ""
    last_price: float = 0
    change: float = 0
    pct_change: float = 0
    market_time: str = ""
    volume: str = ""
    avg_volume_3_mths: str = ""
    market_cap: str = ""


def get_high_yield_stocks() -> list[HighYield]:
    result: list[HighYield] = []

    web_driver.get(URL)
    _ = web_driver.find_element(
        By.CSS_SELECTOR,
        "div > section:nth-child(5) > div > div > table > tbody",
    )
    page_source = web_driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    rs_list = soup.select(
        "div > section:nth-child(5) > div > div > table > tbody",
    )
    for tbl in rs_list:
        rs_row = tbl.select("tr")
        for row in rs_row:
            rs_col = row.select("td")
            stock = HighYield()
            stock.symbol = strip(rs_col[0].text)
            stock.company_name = strip(rs_col[1].text)
            stock.last_price = to_float(rs_col[2].text)
            stock.change = to_float(rs_col[3].text)
            stock.pct_change = to_float(rs_col[4].text)
            stock.market_time = strip(rs_col[5].text)
            stock.volume = strip(rs_col[6].text)
            stock.avg_volume_3_mths = strip(rs_col[7].text)
            stock.market_cap = strip(rs_col[8].text)
            result.append(stock)

    return result
