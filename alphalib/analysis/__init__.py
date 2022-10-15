from dataclasses import dataclass

from alphalib.data_sources.investing import Investing
from alphalib.data_sources.investing import get_stock_details as get_investing
from alphalib.data_sources.nasdaq import Nasdaq
from alphalib.data_sources.nasdaq import get_stock_details as get_nasdaq
from alphalib.data_sources.seeking_alpha import SeekingAlpha
from alphalib.data_sources.seeking_alpha import \
    get_stock_details as get_seeking_alpha
from alphalib.data_sources.yahoo_finance import YahooFinance
from alphalib.data_sources.yahoo_finance import \
    get_stock_details as get_yfinance


@dataclass
class StockAnalysis:
    symbol: str = ""
    yahoo_finance: YahooFinance = YahooFinance()
    investing: Investing = Investing()
    nasdaq: Nasdaq = Nasdaq()
    # seeking_alpha: SeekingAlpha = SeekingAlpha()


def all_sources(symbol: str) -> StockAnalysis:
    assert symbol
    stock_analysis = StockAnalysis()
    stock_analysis.symbol = symbol
    stock_analysis.yahoo_finance = yahoo_finance(symbol)
    stock_analysis.nasdaq = nasdaq(symbol)
    stock_analysis.investing = investing(symbol)
    # stock_analysis.seeking_alpha = seeking_alpha(symbol)
    return stock_analysis


def yahoo_finance(symbol: str) -> YahooFinance:
    assert symbol
    return get_yfinance(symbol)


def seeking_alpha(symbol: str) -> SeekingAlpha:
    assert symbol
    result = get_seeking_alpha(symbol)
    if len(result.dividend_history) == 0:
        return get_seeking_alpha(symbol)
    return result


def nasdaq(symbol: str) -> Nasdaq:
    assert symbol
    return get_nasdaq(symbol)


def investing(symbol: str) -> Investing:
    assert symbol
    return get_investing(symbol)
