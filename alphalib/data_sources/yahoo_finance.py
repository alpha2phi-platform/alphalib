from dataclasses import dataclass
from datetime import datetime

import pandas as pd
import yfinance as yf

from alphalib.utils.convertutils import (TypeConverter, dt_from_ts, join_dicts,
                                         strip)

YFINANCE_URL = "https://finance.yahoo.com/quote/{0}/key-statistics?p={0}"

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


@dataclass
class YahooFinance(TypeConverter):
    symbol: str = ""
    name: str = ""
    exchange: str = ""
    sector: str = ""
    beta: float = 0
    current_price: float | None = 0
    fifty_two_week_low: float | None = 0
    fifty_two_week_high: float | None = 0
    five_year_avg_dividend_yield: float | None = 0
    earnings_date: datetime = datetime.min
    ex_dividend_date: datetime = datetime.min
    dividend_date: datetime = datetime.min
    last_dividend_date: datetime = datetime.min
    forward_eps: float | None = 0
    forward_pe: float | None = 0
    trailing_eps: float | None = 0
    trailing_pe: float | None = 0
    peg_ratio: float | None = 0
    price_to_book: float | None = 0
    free_cash_flow: float | None = 0
    return_on_equity: float | None = 0
    debt_to_equity: float | None = 0
    price_to_sales_trailing_12_months: float | None = 0
    payout_ratio: float | None = 0
    dividend_yield: float | None = 0
    dividend_rate: float | None = 0
    trailing_annual_dividend_rate: float | None = 0
    trailing_annual_dividend_yield: float | None = 0
    yfinance_url: str = ""


def get_stock_details(symbol: str) -> YahooFinance:
    assert symbol

    yahoo_finance = YahooFinance()
    yahoo_finance.symbol = symbol
    yahoo_finance.yfinance_url = YFINANCE_URL.format(symbol)

    ticker = yf.Ticker(symbol)
    stats: dict = ticker.stats()  # type: ignore
    if not stats:
        return yahoo_finance

    key_stats: dict = {}
    key_stats = join_dicts(key_stats, stats, "defaultKeyStatistics")
    key_stats = join_dicts(key_stats, stats, "financialData")
    key_stats = join_dicts(key_stats, stats, "summaryDetail")
    key_stats = join_dicts(key_stats, stats, "price")
    key_stats = join_dicts(key_stats, stats, "summaryProfile")
    key_stats = join_dicts(key_stats, stats, "calendarEvents")

    yahoo_finance.name = strip(key_stats.get("shortName"))
    yahoo_finance.exchange = strip(key_stats.get("exchange"))
    yahoo_finance.sector = strip(key_stats.get("sector"))
    yahoo_finance.beta = key_stats.get("beta")
    yahoo_finance.current_price = key_stats.get("currentPrice")
    yahoo_finance.fifty_two_week_low = key_stats.get("fiftyTwoWeekLow")
    yahoo_finance.fifty_two_week_high = key_stats.get("fiftyTwoWeekHigh")

    earningDts: list = key_stats.get("earnings", {}).get("earningsDate", [])
    if len(earningDts) > 0:
        yahoo_finance.earnings_date = dt_from_ts(earningDts[0])

    yahoo_finance.ex_dividend_date = dt_from_ts(key_stats.get("exDividendDate"))
    yahoo_finance.dividend_date = dt_from_ts(key_stats.get("dividendDate"))
    yahoo_finance.five_year_avg_dividend_yield = key_stats.get(
        "fiveYearAvgDividendYield"
    )
    yahoo_finance.last_dividend_date = dt_from_ts(key_stats.get("lastDividendDate"))
    yahoo_finance.forward_eps = key_stats.get("forwardEps")
    yahoo_finance.forward_pe = key_stats.get("forwardPE")
    yahoo_finance.trailing_eps = key_stats.get("trailingEps")
    yahoo_finance.trailing_pe = key_stats.get("trailingPE")

    yahoo_finance.peg_ratio = key_stats.get("pegRatio")
    yahoo_finance.price_to_book = key_stats.get("priceToBook")
    yahoo_finance.free_cash_flow = key_stats.get("freeCashflow")
    yahoo_finance.return_on_equity = key_stats.get("returnOnEquity")
    yahoo_finance.debt_to_equity = key_stats.get("debtToEquity")
    yahoo_finance.price_to_sales_trailing_12_months = key_stats.get(
        "priceToSalesTrailing12Months"
    )
    yahoo_finance.payout_ratio = key_stats.get("payoutRatio")
    yahoo_finance.dividend_yield = key_stats.get("dividendYield")
    yahoo_finance.dividend_rate = key_stats.get("dividendRate")
    yahoo_finance.trailing_annual_dividend_rate = key_stats.get(
        "trailingAnnualDividendRate"
    )
    yahoo_finance.trailing_annual_dividend_yield = key_stats.get(
        "trailingAnnualDividendYield"
    )

    return yahoo_finance
