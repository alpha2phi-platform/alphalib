from dataclasses import dataclass
from datetime import datetime

import yfinance as yf

from alphalib.utils.convertutils import dt_from_ts, join_dicts, strip


@dataclass
class YahooFinance:
    symbol: str = ""
    name: str = ""
    exchange: str = ""
    sector: str = ""
    currentPrice: float | None = 0
    fiveYearAvgDividendYield: float | None = 0
    earningsDate: datetime = datetime.min
    exDividendDate: datetime = datetime.min
    dividendDate: datetime = datetime.min
    lastDividendDate: datetime = datetime.min
    forwardEps: float | None = 0
    forwardPE: float | None = 0
    trailingEps: float | None = 0
    trailingPE: float | None = 0
    pegRatio: float | None = 0
    priceToBook: float | None = 0
    freeCashflow: float | None = 0
    returnOnEquity: float | None = 0
    debtToEquity: float | None = 0
    priceToSalesTrailing12Months: float | None = 0
    payoutRatio: float | None = 0
    dividendYield: float | None = 0
    dividendRate: float | None = 0


def get_stock_details(symbol: str) -> YahooFinance:
    assert symbol

    yahoo_finance = YahooFinance()
    yahoo_finance.symbol = symbol

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
    yahoo_finance.currentPrice = key_stats.get("currentPrice")

    earningDts: list = key_stats.get("earnings", {}).get("earningsDate", [])
    if len(earningDts) > 0:
        yahoo_finance.earningsDate = dt_from_ts(earningDts[0])

    yahoo_finance.exDividendDate = dt_from_ts(key_stats.get("exDividendDate"))
    yahoo_finance.dividendDate = dt_from_ts(key_stats.get("dividendDate"))
    yahoo_finance.fiveYearAvgDividendYield = key_stats.get("fiveYearAvgDividendYield")
    yahoo_finance.lastDividendDate = dt_from_ts(key_stats.get("lastDividendDate"))
    yahoo_finance.forwardEps = key_stats.get("forwardEps")
    yahoo_finance.forwardPE = key_stats.get("forwardPE")
    yahoo_finance.trailingEps = key_stats.get("trailingEps")
    yahoo_finance.trailingPE = key_stats.get("trailingPE")

    yahoo_finance.pegRatio = key_stats.get("pegRatio")
    yahoo_finance.priceToBook = key_stats.get("priceToBook")
    yahoo_finance.freeCashflow = key_stats.get("freeCashflow")
    yahoo_finance.returnOnEquity = key_stats.get("returnOnEquity")
    yahoo_finance.debtToEquity = key_stats.get("debtToEquity")
    yahoo_finance.priceToSalesTrailing12Months = key_stats.get(
        "priceToSalesTrailing12Months"
    )
    yahoo_finance.payoutRatio = key_stats.get("payoutRatio")
    yahoo_finance.dividendYield = key_stats.get("dividendYield")
    yahoo_finance.dividendRate = key_stats.get("dividendRate")

    return yahoo_finance
