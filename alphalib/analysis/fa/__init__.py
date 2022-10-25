from dataclasses import dataclass

from alphalib.data_sources.investing import Investing
from alphalib.data_sources.investing import get_stock_details as from_investing
from alphalib.data_sources.nasdaq import Nasdaq
from alphalib.data_sources.nasdaq import get_stock_details as from_nasdaq
from alphalib.data_sources.seeking_alpha import SeekingAlpha
from alphalib.data_sources.seeking_alpha import \
    get_stock_details as from_seeking_alpha
from alphalib.data_sources.yahoo_finance import YahooFinance
from alphalib.data_sources.yahoo_finance import \
    get_stock_details as from_yfinance


@dataclass
class FundamentalAnalysis:
    symbol: str = ""
    yahoo_finance: YahooFinance = YahooFinance()
    investing: Investing = Investing()
    nasdaq: Nasdaq = Nasdaq()
    # seeking_alpha: SeekingAlpha = SeekingAlpha()


def all_sources(symbol: str) -> FundamentalAnalysis:
    assert symbol
    fa_analysis = FundamentalAnalysis()
    fa_analysis.symbol = symbol
    fa_analysis.yahoo_finance = yahoo_finance(symbol)
    fa_analysis.nasdaq = nasdaq(symbol)
    fa_analysis.investing = investing(symbol)
    # stock_analysis.seeking_alpha = seeking_alpha(symbol)
    return fa_analysis


def yahoo_finance(symbol: str) -> YahooFinance:
    assert symbol
    return from_yfinance(symbol)


def seeking_alpha(symbol: str) -> SeekingAlpha:
    assert symbol
    result = from_seeking_alpha(symbol)
    if len(result.dividend_history) == 0:
        return from_seeking_alpha(symbol)
    return result


def nasdaq(symbol: str) -> Nasdaq:
    assert symbol
    return from_nasdaq(symbol)


def investing(symbol: str) -> Investing:
    assert symbol
    return from_investing(symbol)
