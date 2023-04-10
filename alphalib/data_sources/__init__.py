from contextlib import closing
from time import sleep

import pandas as pd
import requests

from requests import Response
from requests.adapters import HTTPAdapter

from alphalib.utils import get_project_root
from alphalib.utils.httputils import (
    DEFAULT_HTTP_RETRY,
    DEFAULT_HTTP_TIMEOUT,
    http_headers,
)


def get_stocks() -> pd.DataFrame:
    stock_file = str(
        get_project_root()
        .absolute()
        .joinpath("".join(["data/stock", ".xlsx"]))
        .resolve()
    )
    df = pd.read_excel(stock_file, sheet_name="stock")
    return df.rename(columns=str.lower)


def get_stock_stats() -> pd.DataFrame:
    stock_file = str(
        get_project_root()
        .absolute()
        .joinpath("".join(["data/stock_stats", ".xlsx"]))
        .resolve()
    )
    df = pd.read_excel(stock_file, sheet_name="stock_stats")
    return df.rename(columns=str.lower)


def invoke_api(symbol, api_endpoint, func):
    MAX_RETRIES = 3
    for attempt in range(0, MAX_RETRIES):
        with closing(requests.Session()) as s:
            s.verify = False
            s.mount("https://", HTTPAdapter(max_retries=DEFAULT_HTTP_RETRY))
            r: Response = s.get(
                api_endpoint,
                verify=True,
                headers=http_headers(),
                timeout=DEFAULT_HTTP_TIMEOUT,
            )
            if r.status_code != requests.status_codes.codes["ok"]:
                if attempt == MAX_RETRIES - 1:
                    raise ConnectionError(
                        "ERR: error " + str(r.status_code) + ", try again later."
                    )
                else:
                    sleep(3)
                    continue
            return func(r, symbol, api_endpoint)

    return None
