import pandas as pd

from alphalib.utils import get_project_root


def get_stocks() -> pd.DataFrame:
    stock_file = str(
        get_project_root()
        .absolute()
        .joinpath("".join(["data/stock", ".xlsx"]))
        .resolve()
    )
    df = pd.read_excel(stock_file, sheet_name="stock")
    return df.rename(columns=str.lower)


def get_stock_stats() -> pd.DataFrame:
    stock_file = str(
        get_project_root()
        .absolute()
        .joinpath("".join(["data/stock_stats", ".xlsx"]))
        .resolve()
    )
    df = pd.read_excel(stock_file, sheet_name="stock_stats")
    return df.rename(columns=str.lower)
