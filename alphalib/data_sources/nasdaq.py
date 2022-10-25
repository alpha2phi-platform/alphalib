from dataclasses import dataclass
from datetime import datetime

import pandas as pd
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from alphalib.utils.convertutils import TypeConverter, strip, to_date, to_float
from alphalib.utils.httputils import get_tag_value, web_driver
from alphalib.utils.logger import logger

NASDAQ_URL = "https://www.nasdaq.com/market-activity/stocks/{0}/dividend-history"


@dataclass
class Nasdaq(TypeConverter):
    label: str = ""
    symbol: str = ""
    ex_dividend_date: datetime = datetime.min
    dividend_yield_pct: float = 0
    annual_dividend: float = 0
    pe_ratio: float = 0
    dividend_history: pd.DataFrame = pd.DataFrame()
    nasdaq_url: str = ""


def get_stock_details(symbol: str) -> Nasdaq:
    assert symbol

    download_url = NASDAQ_URL.format(symbol.lower())
    nasdaq = Nasdaq()
    nasdaq.symbol = symbol
    nasdaq.nasdaq_url = download_url
    web_driver.get(download_url)
    # WebDriverWait(web_driver, DEFAULT_HTTP_TIMEOUT).until(
    #     EC.presence_of_element_located(
    #         (By.CSS_SELECTOR, "div > table > tbody > tr:nth-child(2) > td:nth-child(2)")
    #     )
    try:
        web_driver.find_element(
            By.CSS_SELECTOR, "div.dividend-history.dividend-history--loaded"
        )
    except NoSuchElementException:
        logger.warning(f"Unable to get details for {symbol}")
        return nasdaq

    page_source = web_driver.page_source
    soup = BeautifulSoup(page_source, "lxml")

    # Get the stock label
    nasdaq.label = get_tag_value(soup, "div.dividend-history__heading > h1", strip)

    # Ex dividend date
    nasdaq.ex_dividend_date = get_tag_value(
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
        div_hist.extend(
            [
                to_date(rs_ex_dt[idx].text),
                strip(rs_type[idx].text),
                to_float(rs_cash_amt[idx].text),
                to_date(rs_decl_dt[idx].text),
                to_date(rs_rec_dt[idx].text),
                to_date(rs_payment_dt[idx].text),
            ]
        )
        div_hists.extend([div_hist])

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
