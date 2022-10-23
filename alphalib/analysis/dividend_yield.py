from dataclasses import dataclass
from datetime import datetime

import pandas as pd
from dateutil import relativedelta

from alphalib.analysis import get_nasdaq, get_yfinance
from alphalib.data_sources import get_stock_stats
from alphalib.data_sources.nasdaq import Nasdaq
from alphalib.data_sources.yahoo_finance import YahooFinance
from alphalib.dataset.high_yield import get_high_yield_stocks
from alphalib.utils.convertutils import set_fields
from alphalib.utils.dateutils import from_epoch_time
from alphalib.utils.logger import logger


@dataclass
class YieldAnalysis(YahooFinance, Nasdaq):
    source: str = ""


def recommend_stocks(by="sector", filter_earnings_dt=True) -> list[YieldAnalysis]:
    stock_stats: pd.DataFrame = get_stock_stats()
    stock_stats["lastdividenddate"] = stock_stats["lastdividenddate"].apply(
        from_epoch_time
    )
    yield_stocks = pd.DataFrame()
    current_year = datetime.now().year
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

    yield_stocks = stock_stats[
        (stock_stats["lastdividenddate"].dt.year == current_year)
        & (stock_stats["fiveyearavgdividendyield"].notnull())
    ]

    # Stocks from Excel dataset
    if by == "sector":
        yield_stocks = yield_stocks.groupby(by=["sector"]).head(5)
    else:
        yield_stocks = yield_stocks.head(20)

    # Stocks from Yahoo finance list
    yf_stocks = get_high_yield_stocks()

    # Check yield stocks and recommend stocks
    rec_stocks: list[YieldAnalysis] = []
    for symbol in yield_stocks["symbol"]:
        logger.info(f"Getting info for {symbol}")
        yf_stock_info = get_yfinance(symbol)
        nasdaq_stock_info = get_nasdaq(symbol)
        rec_stock = YieldAnalysis()
        rec_stock.source = "dataset"
        set_fields(yf_stock_info, rec_stock)
        set_fields(nasdaq_stock_info, rec_stock)
        rec_stocks.append(rec_stock)

    for stock in yf_stocks:
        if stock.symbol not in yield_stocks["symbol"]:
            logger.info(f"Getting info for {stock.symbol}")
            yf_stock_info = get_yfinance(stock.symbol)
            nasdaq_stock_info = get_nasdaq(stock.symbol)
            rec_stock = YieldAnalysis()
            rec_stock.source = "yahoo_finance"
            set_fields(yf_stock_info, rec_stock)
            set_fields(nasdaq_stock_info, rec_stock)
            rec_stocks.append(rec_stock)

    # Sort by dividend yield %
    rec_stocks.sort(key=lambda s: s.dividend_yield_pct, reverse=True)

    # Only earnings date in current and next month
    if filter_earnings_dt:
        current_month = datetime.now()
        next_month = current_month + relativedelta.relativedelta(months=1)
        rec_stocks = [
            s
            for s in rec_stocks
            if (
                s.earnings_date.year == current_month.year
                and s.earnings_date.month == current_month.month
            )
            or (
                s.earnings_date.year == next_month.year
                and s.earnings_date.month == next_month.month
            )
        ]

    return rec_stocks
