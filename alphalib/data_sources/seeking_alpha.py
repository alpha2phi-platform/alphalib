import time
from contextlib import closing
from dataclasses import dataclass

import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from alphalib.utils.convertutils import TypeConverter, strip, to_date, to_float
from alphalib.utils.httputils import (DEFAULT_HTTP_RETRY, DEFAULT_HTTP_TIMEOUT,
                                      get_driver, http_headers)
from alphalib.utils.logger import logger

SEEKING_ALPHA_URL = "https://seekingalpha.com/symbol/{0}/dividends/history"

SEEKING_ALPHA_DIVIDEND_HISTORY_API_ENDPOINT = "https://seekingalpha.com/api/v3/symbols/{0}/dividend_history?group_by=quarterly&sort=-date"


@dataclass
class SeekingAlpha(TypeConverter):
    symbol: str = ""
    seeking_alpha_url: str = ""
    dividend_history: pd.DataFrame = pd.DataFrame()


def get_dividend_history(symbol: str) -> SeekingAlpha:
    assert symbol

    api_endpoint = SEEKING_ALPHA_DIVIDEND_HISTORY_API_ENDPOINT.format(symbol.upper())
    with closing(requests.Session()) as s:
        s.verify = False
        s.mount("https://", HTTPAdapter(max_retries=DEFAULT_HTTP_RETRY))
        r = s.get(
            api_endpoint, verify=True, headers=http_headers(), timeout=DEFAULT_HTTP_TIMEOUT
        )
        if r.status_code != requests.status_codes.codes["ok"]:
            raise ConnectionError(
                "ERR: error " + str(r.status_code) + ", try again later."
            )
        # Parse the JSON output
        print(r.text)
        result = json.load(r.text)
        print(result)

    sa = SeekingAlpha()
    sa.symbol = symbol
    sa.seeking_alpha_url = api_endpoint

    return sa


def _get_stock_details(symbol: str) -> SeekingAlpha:
    assert symbol

    download_url = SEEKING_ALPHA_URL.format(symbol.upper())
    seekingAlpha = SeekingAlpha()
    seekingAlpha.symbol = symbol
    seekingAlpha.seeking_alpha_url = download_url

    driver = get_driver(download_url)
    try:
        driver.find_element(
            By.CSS_SELECTOR, "div > table > tbody > tr:nth-child(n+2) > td:nth-child(2)"
        )
    except NoSuchElementException:
        logger.warn(f"Unable to get details for {symbol}")
        return seekingAlpha

    time.sleep(5)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")

    # Dividend history
    rs_decl_dt = soup.select(
        "div > table > tbody > tr:nth-child(n+2) > td:nth-child(2)"
    )
    rs_ex_div_dt = soup.select(
        "div > table > tbody > tr:nth-child(n+2) > td:nth-child(3)"
    )
    rs_rec_dt = soup.select("div > table > tbody > tr:nth-child(n+2) > td:nth-child(4)")
    rs_pay_dt = soup.select("div > table > tbody > tr:nth-child(n+2) > td:nth-child(5)")
    rs_freq = soup.select("div > table > tbody > tr:nth-child(n+2) > td:nth-child(6)")
    rs_amt = soup.select("div > table > tbody > tr:nth-child(n+2) > td:nth-child(7)")
    rs_adj_amt = soup.select(
        "div > table > tbody > tr:nth-child(n+2) > td:nth-child(8)"
    )

    div_hists = []
    # assert (
    #     len(rs_decl_dt)
    #     == len(rs_ex_div_dt)
    #     == len(rs_rec_dt)
    #     == len(rs_pay_dt)
    #     == len(rs_freq)
    #     == len(rs_amt)
    #     == len(rs_adj_amt)
    # )
    for idx in range(0, len(rs_adj_amt)):
        div_hist = []
        adj_amt = rs_adj_amt[idx].text
        if strip(adj_amt):
            div_hist.extend(
                [
                    to_date(rs_decl_dt[idx].text),
                    to_date(rs_ex_div_dt[idx].text),
                    to_date(rs_rec_dt[idx].text),
                    to_date(rs_pay_dt[idx].text),
                    strip(rs_freq[idx].text),
                    to_float(rs_amt[idx].text),
                    to_float(adj_amt),
                ]
            )

        if len(div_hist) > 0:
            div_hists.extend([div_hist])

    seekingAlpha.dividend_history = pd.DataFrame(
        div_hists,
        columns=[
            "declaration_date",
            "ex_dividend_date",
            "record_date",
            "pay_date",
            "frequency",
            "amount",
            "adj_amount",
        ],
    )
    return seekingAlpha
