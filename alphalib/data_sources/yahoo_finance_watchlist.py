from contextlib import closing
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

from alphalib.utils.convertutils import TypeConverter, strip, to_float
from alphalib.utils.httputils import (DEFAULT_HTTP_RETRY, DEFAULT_HTTP_TIMEOUT,
                                      http_headers)


@dataclass
class WatchedStock(TypeConverter):
    symbol: str = ""
    company_name: str = ""
    last_price: float = 0
    change: float = 0
    pct_change: float = 0
    market_time: str = ""
    volume: str = ""
    avg_volume_3_mths: str = ""
    market_cap: str = ""


def get_watchlist(url: str) -> list[WatchedStock]:
    watchlist: list[WatchedStock] = []

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
        rs_list = soup.select(
            "#Col1-0-WatchlistDetail-Proxy > div > section:nth-child(5) > div > div > table > tbody"
        )
        for tbl in rs_list:
            rs_row = tbl.select("tr")
            for row in rs_row:
                rs_col = row.select("td")
                stock = WatchedStock()
                stock.symbol = strip(rs_col[0].text)
                stock.company_name = strip(rs_col[1].text)
                stock.last_price = to_float(rs_col[2].text)
                stock.change = to_float(rs_col[3].text)
                stock.pct_change = to_float(rs_col[4].text)
                stock.market_time = strip(rs_col[5].text)
                stock.volume = strip(rs_col[6].text)
                stock.avg_volume_3_mths = strip(rs_col[7].text)
                stock.market_cap = strip(rs_col[8].text)
                watchlist.append(stock)

    return watchlist
