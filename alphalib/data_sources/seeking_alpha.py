from dataclasses import dataclass

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from alphalib.utils.convertutils import strip, to_date, to_float
from alphalib.utils.httputils import DEFAULT_HTTP_TIMEOUT, web_driver

URL = "https://seekingalpha.com/symbol/{0}/dividends/history"


@dataclass
class SeekingAlpha:
    symbol: str = ""
    url: str = ""
    dividend_history: pd.DataFrame = pd.DataFrame()


def get_stock_details(symbol: str) -> SeekingAlpha:
    assert symbol is not None

    download_url = URL.format(symbol.upper())
    seekingAlpha = SeekingAlpha()
    seekingAlpha.symbol = symbol
    seekingAlpha.url = download_url
    web_driver.get(download_url)
    WebDriverWait(web_driver, DEFAULT_HTTP_TIMEOUT).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div > table > tbody > tr:nth-child(2) > td:nth-child(2)")
        )
    )
    page_source = web_driver.page_source
    soup = BeautifulSoup(page_source, "lxml")

    # Dividend history
    rs_decl_dt = soup.select("div > table > tbody > tr > td:nth-child(2)")
    rs_ex_div_dt = soup.select("div > table > tbody > tr > td:nth-child(3)")
    rs_rec_dt = soup.select("div > table > tbody > tr > td:nth-child(4)")
    rs_pay_dt = soup.select("div > table > tbody > tr > td:nth-child(5)")
    rs_freq = soup.select("div > table > tbody > tr > td:nth-child(6)")
    rs_amt = soup.select("div > table > tbody > tr > td:nth-child(7)")
    rs_adj_amt = soup.select("div > table > tbody > tr > td:nth-child(8)")

    div_hists = []
    for idx in range(0, len(rs_decl_dt)):
        div_hist = []
        if strip(rs_decl_dt[idx].text):
            div_hist.append(to_date(rs_decl_dt[idx].text))
            div_hist.append(to_date(rs_ex_div_dt[idx].text))
            div_hist.append(to_date(rs_rec_dt[idx].text))
            div_hist.append(to_date(rs_pay_dt[idx].text))
            div_hist.append(strip(rs_freq[idx].text))
            div_hist.append(to_float(rs_amt[idx].text))
            div_hist.append(to_float(rs_adj_amt[idx].text))

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
