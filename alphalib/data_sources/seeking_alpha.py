import time
from dataclasses import dataclass

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from alphalib.utils.convertutils import TypeConverter, strip, to_date, to_float
from alphalib.utils.httputils import web_driver

URL = "https://seekingalpha.com/symbol/{0}/dividends/history"


@dataclass
class SeekingAlpha(TypeConverter):
    symbol: str = ""
    url: str = ""
    dividend_history: pd.DataFrame = pd.DataFrame()


def get_stock_details(symbol: str) -> SeekingAlpha:
    assert symbol

    download_url = URL.format(symbol.upper())
    seekingAlpha = SeekingAlpha()
    seekingAlpha.symbol = symbol
    seekingAlpha.url = download_url

    web_driver.get(download_url)
    _ = web_driver.find_element(
        By.CSS_SELECTOR, "div > table > tbody > tr:nth-child(n+2) > td:nth-child(2)"
    )
    # for c in web_driver.get_cookies():
    #     print(c)

    time.sleep(5)
    page_source = web_driver.page_source
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
    assert (
        len(rs_decl_dt)
        == len(rs_ex_div_dt)
        == len(rs_rec_dt)
        == len(rs_pay_dt)
        == len(rs_freq)
        == len(rs_amt)
        == len(rs_adj_amt)
    )
    for idx in range(0, len(rs_adj_amt)):
        div_hist = []
        adj_amt = rs_adj_amt[idx].text
        if strip(adj_amt):
            div_hist.append(to_date(rs_decl_dt[idx].text))
            div_hist.append(to_date(rs_ex_div_dt[idx].text))
            div_hist.append(to_date(rs_rec_dt[idx].text))
            div_hist.append(to_date(rs_pay_dt[idx].text))
            div_hist.append(strip(rs_freq[idx].text))
            div_hist.append(to_float(rs_amt[idx].text))
            div_hist.append(to_float(adj_amt))

        if len(div_hist) > 0:
            div_hists.append(div_hist)

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
