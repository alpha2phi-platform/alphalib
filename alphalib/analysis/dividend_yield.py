from datetime import datetime

import pandas as pd

from alphalib.data_sources import get_stock_stats
from alphalib.utils.dateutils import from_epoch_time
from alphalib.dataset.high_yield import get_high_yield_stocks


def recommend_stocks(by="sector", limit=20) -> None:
    stock_stats: pd.DataFrame = get_stock_stats()
    stock_stats["lastdividenddate"] = stock_stats["lastdividenddate"].apply(
        from_epoch_time
    )
    yield_stocks = pd.DataFrame()
    current_year = datetime.now().year
    if by == "all":
        stock_stats.sort_values(
            by=["fiveyearavgdividendyield"], ascending=False, inplace=True
        )
    elif by == "sector":
        stock_stats.sort_values(
            by=["sector", "fiveyearavgdividendyield"], ascending=False, inplace=True
        )
    else:
        raise NotImplementedError(f"By {by} is not implemented.")

    yield_stocks = stock_stats[
        (stock_stats["lastdividenddate"].dt.year == current_year)
        & (stock_stats["fiveyearavgdividendyield"].notnull())
    ]
    if by == "sector":
        yield_stocks = yield_stocks.groupby(by=["sector"]).head(10)
    else:
        yield_stocks = yield_stocks.head(30)

    yf_yield_stocks = get_high_yield_stocks()
