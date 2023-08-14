import pandas as pd
import numpy as np
import time
from datetime import datetime, timezone
from alphalib.data_sources import get_stock_stats


def select_stocks() -> pd.DataFrame:
    df_stock_stats = get_stock_stats()
    return df_stock_stats
