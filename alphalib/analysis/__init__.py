from dataclasses import dataclass

from alphalib.data_sources.investing import Investing
from alphalib.data_sources.nasdaq import Nasdaq, get_stock_details as get_nasdaq
from alphalib.data_sources.seeking_alpha import SeekingAlpha, get_stock_details as get_seeking_alpha
from alphalib.data_sources.yahoo_finance import YahooFinance, get_stock_details as get_yfinance


@dataclass
class StockAnalysis:
    symbol: str = ""
    yahooFinance: YahooFinance = YahooFinance()
    investing: Investing = Investing()
    nasdaq: Nasdaq = Nasdaq()
    seeking_alpha: SeekingAlpha = SeekingAlpha()


def analyze_stock(symbol: str) -> StockAnalysis:
    assert symbol is not None

    stock_analysis = StockAnalysis()
    stock_analysis.symbol = symbol
    stock_analysis.yahooFinance = get_yfinance(symbol)
    stock_analysis.seeking_alpha = get_seeking_alpha(symbol)
    stock_analysis.nasdaq = get_nasdaq(symbol)

    return stock_analysis
