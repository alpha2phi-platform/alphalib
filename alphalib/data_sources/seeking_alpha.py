from contextlib import closing
from dataclasses import dataclass

import pandas as pd
import requests
from requests.adapters import HTTPAdapter

from alphalib.utils.convertutils import TypeConverter
from alphalib.utils.httputils import (DEFAULT_HTTP_RETRY, DEFAULT_HTTP_TIMEOUT,
                                      http_headers)

SEEKING_ALPHA_DIVIDEND_HISTORY_API_ENDPOINT = "https://seekingalpha.com/api/v3/symbols/{0}/dividend_history?group_by=quarterly&sort=-date"


@dataclass
class SeekingAlpha(TypeConverter):
    symbol: str = ""
    seeking_alpha_url: str = ""
    dividend_history: pd.DataFrame = pd.DataFrame()


def get_stock_info(symbol: str) -> SeekingAlpha:
    assert symbol

    api_endpoint = SEEKING_ALPHA_DIVIDEND_HISTORY_API_ENDPOINT.format(symbol.upper())
    sa = SeekingAlpha()
    sa.symbol = symbol
    sa.seeking_alpha_url = api_endpoint
    with closing(requests.Session()) as s:
        s.verify = False
        s.mount("https://", HTTPAdapter(max_retries=DEFAULT_HTTP_RETRY))
        r = s.get(
            api_endpoint,
            verify=True,
            headers=http_headers(),
            timeout=DEFAULT_HTTP_TIMEOUT,
        )
        if r.status_code != requests.status_codes.codes["ok"]:
            raise ConnectionError(
                "ERR: error " + str(r.status_code) + ", try again later."
            )
        # Parse the JSON output
        results = []
        json: dict = r.json()
        for row in json["data"]:
            results.append(row["attributes"])
        if len(results) > 0:
            sa.dividend_history = pd.json_normalize(results)

    return sa
