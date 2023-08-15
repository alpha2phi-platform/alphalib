import pandas as pd
from alphalib.data_sources import get_stock_stats


def select_stocks() -> pd.DataFrame:
    df_stock_stats = get_stock_stats()
    return df_stock_stats
