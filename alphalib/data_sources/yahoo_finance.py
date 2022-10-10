from dataclasses import dataclass
from datetime import datetime

import yfinance as yf

from alphalib.utils.convertutils import dt_from_ts


@dataclass
class YahooFinance:
    symbol: str = ""
    name: str = ""
    exchange: str = ""
    sector: str = ""
    currentPrice: float = 0
    earningsDate: datetime = datetime.min
    exDividendDate: datetime = datetime.min
    dividendDate: datetime = datetime.min


def get_stock_details(symbol: str) -> YahooFinance:
    assert symbol is not None

    yahoo_finance = YahooFinance()
    yahoo_finance.symbol = symbol

    ticker = yf.Ticker(symbol)
    stock_stats = ticker.stats()
    yahoo_finance.name = stock_stats["price"]["shortName"]  # type: ignore
    yahoo_finance.exchange = stock_stats["price"]["exchange"]  # type: ignore
    yahoo_finance.sector = stock_stats["summaryProfile"]["sector"]  # type: ignore
    yahoo_finance.currentPrice = stock_stats["financialData"]["currentPrice"]  # type: ignore
    calendar_events = stock_stats["calendarEvents"]  # type: ignore
    yahoo_finance.earningsDate = dt_from_ts(
        calendar_events["earnings"]["earningsDate"][0]
    )
    yahoo_finance.exDividendDate = dt_from_ts(calendar_events["exDividendDate"])
    yahoo_finance.dividendDate = dt_from_ts(calendar_events["dividendDate"])

    return yahoo_finance
