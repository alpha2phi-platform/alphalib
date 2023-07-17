from dataclasses import dataclass

import pandas as pd

from alphalib.data_sources.nasdaq import Nasdaq


@dataclass(kw_only=True)
class DividendAnalysis(Nasdaq):
    interval: str = ""  # MONTHLY, QUARTERLY, YEARLY
    result: pd.DataFrame = None


def derive_dividend_interval(interval: float):
    if interval <= 45:
        return "MONTHLY"
    if interval <= 110:
        return "QUARTERLY"
    return "YEARLY"


def calculate_avg_dividend_interval(
    dividend_history: pd.DataFrame,
) -> (pd.DataFrame, float):
    dividend_history["interval"] = abs(dividend_history["exOrEffDate"].diff().dt.days)
    intervals = dividend_history.groupby(
        by=["exOrEffDate"], as_index=False, sort=False
    )["interval"].max()
    return intervals, intervals.head(12)["interval"].mean()


def convert_fields(dividend_history: pd.DataFrame):
    dividend_history["exOrEffDate"] = pd.to_datetime(
        dividend_history["exOrEffDate"], format="%m/%d/%Y"
    )


def analyze_historical_prices(intervals: pd.DataFrame) -> pd.DataFrame:
    # Analyze the historical close prices for the first 12 months
    dividend_dates = intervals["exOrEffDate"].head(12).to_list()
    dates_interval = [
        dividend_dates[i : i + 2] for i in range(0, len(dividend_dates), 1)
    ]
    for interval in dates_interval:
        if len(interval) == 2:
            print(interval)

    # ticker = Ticker(symbol)
    # ticker.session.close()


def dividend_analysis(symbol: str) -> DividendAnalysis:
    # For testing
    result: DividendAnalysis = DividendAnalysis()
    dividend_history = pd.read_excel(f"data/{symbol}.xlsx")

    # Get dividend history
    # stock_dividend_info: Nasdaq = get_dividend_info(symbol)
    # result: DividendAnalysis = DividendAnalysis(**vars(stock_dividend_info))
    # dividend_history = result.dividend_history

    convert_fields(dividend_history)
    intervals, mean_interval = calculate_avg_dividend_interval(dividend_history)
    result.interval = derive_dividend_interval(mean_interval)

    # print(result)
