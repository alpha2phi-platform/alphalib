from dataclasses import dataclass
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from alphalib.utils.convertutils import strip, to_date, to_float
from alphalib.utils.httputils import (DEFAULT_HTTP_TIMEOUT, get_tag_value,
                                      web_driver)

URL = "https://www.nasdaq.com/market-activity/stocks/{0}/dividend-history"


@dataclass
class Nasdaq:
    label: str = ""
    symbol: str = ""
    exDividendDate: datetime = datetime.min
    dividend_yield_pct: float = 0
    annual_dividend: float = 0
    pe_ratio: float = 0
    dividend_history: pd.DataFrame = pd.DataFrame()
    url: str = ""


def get_dividend_history(symbol: str) -> Nasdaq:
    assert symbol is not None

    download_url = URL.format(symbol.lower())
    nasdaq = Nasdaq()
    nasdaq.symbol = symbol
    nasdaq.url = download_url
    web_driver.get(download_url)
    WebDriverWait(web_driver, DEFAULT_HTTP_TIMEOUT).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.dividend-history.dividend-history--loaded")
        )
    )
    page_source = web_driver.page_source
    soup = BeautifulSoup(page_source, "lxml")

    # Get the stock label
    nasdaq.label = get_tag_value(soup, "div.dividend-history__heading > h1", strip)

    # Ex dividend date
    nasdaq.exDividendDate = get_tag_value(
        soup,
        "ul > li:nth-child(1) > span.dividend-history__summary-item__value",
        to_date,
    )

    # Dividend yield
    nasdaq.dividend_yield_pct = get_tag_value(
        soup,
        "ul > li:nth-child(2) > span.dividend-history__summary-item__value",
        to_float,
    )

    # Annual dividend
    nasdaq.annual_dividend = get_tag_value(
        soup,
        "ul > li:nth-child(3) > span.dividend-history__summary-item__value",
        to_float,
    )

    # PE ratio
    nasdaq.pe_ratio = get_tag_value(
        soup,
        "ul > li:nth-child(4) > span.dividend-history__summary-item__value",
        to_float,
    )

    # Dividend history
    rs_ex_dt = soup.select(
        "div.dividend-history__table-container > table > tbody > tr > th"
    )
    rs_type = soup.select(
        "div.dividend-history__table-container > table > tbody > tr > td.dividend-history__cell.dividend-history__cell--type"
    )
    rs_cash_amt = soup.select(
        "div.dividend-history__table-container > table > tbody > tr > td.dividend-history__cell.dividend-history__cell--amount"
    )
    rs_decl_dt = soup.select(
        "div.dividend-history__table-container > table > tbody > tr > td.dividend-history__cell.dividend-history__cell--declarationDate"
    )
    rs_rec_dt = soup.select(
        "div.dividend-history__table-container > table > tbody > tr > td.dividend-history__cell.dividend-history__cell--recordDate"
    )
    rs_payment_dt = soup.select(
        "div.dividend-history__table-container > table > tbody > tr > td.dividend-history__cell.dividend-history__cell--paymentDate"
    )

    assert (
        len(rs_ex_dt)
        == len(rs_type)
        == len(rs_cash_amt)
        == len(rs_decl_dt)
        == len(rs_rec_dt)
        == len(rs_payment_dt)
    )
    div_hists = []
    for idx in range(0, len(rs_ex_dt)):
        div_hist = []
        div_hist.append(to_date(rs_ex_dt[idx].text))
        div_hist.append(strip(rs_type[idx].text))
        div_hist.append(to_float(rs_cash_amt[idx].text))
        div_hist.append(to_date(rs_decl_dt[idx].text))
        div_hist.append(to_date(rs_rec_dt[idx].text))
        div_hist.append(to_date(rs_payment_dt[idx].text))

        div_hists.append(div_hist)

    nasdaq.dividend_history = pd.DataFrame(
        div_hists,
        columns=[
            "ex_eff_date",
            "type",
            "cash_amount",
            "declaration_date",
            "record_date",
            "payment_date",
        ],
    )
    return nasdaq
