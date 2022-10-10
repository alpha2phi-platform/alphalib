from dataclasses import dataclass
from datetime import datetime

import pandas as pd


@dataclass
class YahooFinance:
    currentPrice: float = 0
    earningsDate: datetime = datetime.min
    exDividendDate: datetime = datetime.min
    dividendDate: datetime = datetime.min
    dividendHistory: pd.DataFrame = pd.DataFrame()
