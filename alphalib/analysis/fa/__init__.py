from dataclasses import dataclass

from alphalib.data_sources.investing import Investing
from alphalib.data_sources.nasdaq import Nasdaq
from alphalib.data_sources.seeking_alpha import SeekingAlpha
from alphalib.data_sources.yahoo_finance import YahooFinance


@dataclass
class FundamentalAnalysis:
    symbol: str = ""
    yahoo_finance: YahooFinance = YahooFinance()
    investing: Investing = Investing()
    nasdaq: Nasdaq = Nasdaq()
    seeking_alpha: SeekingAlpha = SeekingAlpha()
