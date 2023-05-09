from dataclasses import dataclass
from datetime import datetime

import pandas as pd

from alphalib.analysis.sentiment import finwiz_score
from alphalib.data_sources import get_stock_stats, nasdaq, seeking_alpha, yahoo_query
from alphalib.data_sources.nasdaq import Nasdaq
from alphalib.data_sources.seeking_alpha import SeekingAlpha
from alphalib.data_sources.yahoo_query import YahooQuery
from alphalib.data_sources.yahoo_finance_watchlist import get_watchlist
from alphalib.utils.dateutils import from_epoch_time, month_from
from alphalib.utils.logger import logger

SEEKING_ALPHA_STOCK_URL = "https://seekingalpha.com/symbol/{0}"

YAHOO_FINANCE_HIGH_YIELD_STOCK_URL = (
    "https://finance.yahoo.com/u/yahoo-finance/watchlists/high-yield-dividend-stocks/"
)

TARGET_YIELD = 15


@dataclass
class RecommendedStock:
    symbol: str = ""
    source: str = ""
    sentiment_score: float = 0
    yq: YahooQuery = None
    nas: Nasdaq = None
    sa: SeekingAlpha = None
    info_url: str = ""


def _get_stock_sentiment(symbol: str, months_ago=-2) -> float:
    try:
        past_months = month_from(months_ago)
        sentiment_result = finwiz_score(symbol)
        return sentiment_result[sentiment_result["date"] >= past_months.date()][
            "compound"
        ].mean()
    except Exception:
        return 0


def _filter_next_earning_dt(stocks: list[RecommendedStock], nearest_earning_mth=2):
    current_month = datetime.now()
    next_month = month_from(nearest_earning_mth + 1)
    stocks = [
        s
        for s in stocks
        if (current_month < s.yq.earnings_date < next_month)
        or (current_month < s.sa.estimated_earning_date < next_month)
    ]
    return stocks


def _get_stock_info(symbol: str, stock: RecommendedStock):
    stock.symbol = symbol
    stock.yq = yahoo_query.get_stock_info(symbol)
    stock.nas = nasdaq.get_stock_info(symbol)
    stock.sa = seeking_alpha.get_stock_info(symbol)
    stock.info_url = SEEKING_ALPHA_STOCK_URL.format(symbol)
    return stock


def recommend_stocks_from_watchlist(
    watchlist_url=YAHOO_FINANCE_HIGH_YIELD_STOCK_URL,
    filter_earnings_dt=True,
    sentiment=True,
) -> list[RecommendedStock]:
    # Stocks from Yahoo finance watchlist
    watchlist = get_watchlist(watchlist_url)
    rec_stocks: list[RecommendedStock] = []
    for stock in watchlist:
        logger.info(f"Getting info for {stock.symbol}")
        rec_stock = RecommendedStock()
        rec_stock.source = watchlist_url
        _get_stock_info(stock.symbol, rec_stock)
        if sentiment:
            rec_stock.sentiment_score = _get_stock_sentiment(stock.symbol)

        rec_stocks.append(rec_stock)

    # Sort by dividend yield %
    # rec_stocks.sort(key=lambda s: s.dividend_yield_pct, reverse=True)
    rec_stocks.sort(key=lambda s: s.yq.trailing_annual_dividend_yield, reverse=True)

    # Only earnings date in current and next month
    if filter_earnings_dt:
        rec_stocks = _filter_next_earning_dt(rec_stocks)
    return rec_stocks


def recommend_stocks_from_dataset(
    by="sector", filter_earnings_dt=True, sentiment=True, target_yield=TARGET_YIELD
) -> list[RecommendedStock]:
    stock_stats: pd.DataFrame = get_stock_stats()
    stock_stats["lastdividenddate"] = stock_stats["lastdividenddate"].apply(
        from_epoch_time
    )
    yield_stocks = pd.DataFrame()
    if by == "all":
        logger.info("Analyze all stocks...")
        stock_stats.sort_values(
            by=["fiveyearavgdividendyield"], ascending=False, inplace=True
        )
    elif by == "sector":
        logger.info("Analyze stocks by sector")
        stock_stats.sort_values(
            by=["sector", "fiveyearavgdividendyield"], ascending=False, inplace=True
        )
    else:
        raise NotImplementedError(f"By {by} is not implemented.")

    yield_stocks = stock_stats[(stock_stats["fiveyearavgdividendyield"].notnull())]

    # Stocks from Excel dataset
    if by == "sector":
        yield_stocks = (
            yield_stocks[(yield_stocks["fiveyearavgdividendyield"] >= target_yield)]
            .groupby(by=["sector"])
            .head(1000)
        )
    else:
        yield_stocks = yield_stocks[
            (yield_stocks["fiveyearavgdividendyield"] >= target_yield)
        ]

    # Check yield stocks and recommend stocks
    rec_stocks: list[RecommendedStock] = []
    for symbol in yield_stocks["symbol"]:
        logger.info(f"Getting info for {symbol}")
        rec_stock = RecommendedStock()
        rec_stock.source = "dataset"
        _get_stock_info(symbol, rec_stock)

        if sentiment:
            rec_stock.sentiment_score = _get_stock_sentiment(symbol)

        rec_stocks.append(rec_stock)

    # Sort by dividend yield %
    # rec_stocks.sort(key=lambda s: s.dividend_yield_pct, reverse=True)
    rec_stocks.sort(key=lambda s: s.yq.trailing_annual_dividend_yield, reverse=True)

    # Only earnings date in current and next month
    if filter_earnings_dt:
        rec_stocks = _filter_next_earning_dt(rec_stocks)

    return rec_stocks
