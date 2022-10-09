import time
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from requests.adapters import HTTPAdapter

from ..utils.httputils import (DEFAULT_HTTP_RETRY, DEFAULT_HTTP_TIMEOUT,
                               http_headers)


@dataclass
class Nasdaq:
    label: str = ""
    exDividendDate: datetime = datetime.min
    dividend_yield_pct: float = 0
    annual_dividend: float = 0
    pe_ratio: float = 0
    dividend_history: pd.DataFrame = pd.DataFrame()


def get_dividend_history(url: str) -> Nasdaq:
    assert url is not None

    nasdaq = Nasdaq()
    with closing(requests.Session()) as s:
        s.verify = False
        s.mount("https://", HTTPAdapter(max_retries=DEFAULT_HTTP_RETRY))
        r = s.get(
            url, verify=True, headers=http_headers(), timeout=DEFAULT_HTTP_TIMEOUT
        )
        if r.status_code != requests.status_codes.codes["ok"]:
            raise ConnectionError(
                "ERR: error " + str(r.status_code) + ", try again later."
            )
        soup = BeautifulSoup(r.text, "lxml")
        print(r.text)

        # Get the stock label
        tag: Tag | None = soup.select_one("div.dividend-history__heading > h1")
        if tag:
            nasdaq.label = tag.text

        # Get ex dividend date
        tag = soup.select_one(
            "ul > li:nth-child(1) > span.dividend-history__summary-item__value"
        )
        if tag:
            print(tag.text)
        else:
            print("not found")
            # nasdaq.exDividendDate =

    return nasdaq
