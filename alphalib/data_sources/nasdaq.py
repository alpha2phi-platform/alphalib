from dataclasses import dataclass
from datetime import datetime

import pandas as pd
import requests
from lxml.cssselect import CSSSelector
from lxml.html import fromstring
from requests.adapters import HTTPAdapter

from ..utils.httputils import (DEFAULT_HTTP_RETRY, DEFAULT_HTTP_TIMEOUT,
                               http_headers)

name_selector = CSSSelector("div.dividend-history__heading > h1")


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

    s = requests.Session()
    s.mount("https://", HTTPAdapter(max_retries=DEFAULT_HTTP_RETRY))
    r = s.get(url, verify=True,headers=http_headers(), timeout=DEFAULT_HTTP_TIMEOUT)
    if r.status_code != 200:
        raise ConnectionError(
            "ERR: error " + str(r.status_code) + ", try again later."
        )
    h = fromstring(r.text)

    # Get name
    elems = name_selector(h)
    if elems:
        nasdaq.label = elems[0].text  # type: ignore

    # elem = res.html.find("div.dividend-history__heading > h1", first=True)
    # if elem:

    # # Ex dividend date
    # elem = res.html.find(
    #         "ul > li:nth-child(1) > span.dividend-history__summary-item__value" , first=True,
    # )
    # print(elem)  # type: ignore

    return nasdaq
