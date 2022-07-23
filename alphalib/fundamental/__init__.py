import sqlite3
from dataclasses import dataclass

import pandas as pd

from ..data_sources import get_stocks


@dataclass
class Fundamental:
    """Perform fundamental analysis for stocks."""

    # yfinance or investpy
    data_source: str = "yfinance"

    # Default to US
    country: str = "united states"

    def get_stocks(self) -> None:
        pass
