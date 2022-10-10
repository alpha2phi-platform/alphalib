from dataclasses import dataclass

import pandas as pd


@dataclass
class Investing:
    dividendHistory: pd.DataFrame = pd.DataFrame()
