import pandas as pd

from alphalib.utils import get_project_root


def get_stocks() -> pd.DataFrame:
    stock_file = str(
        get_project_root()
        .absolute()
        .joinpath("".join(["data/stock", ".xlsx"]))
        .resolve()
    )
    return pd.read_excel(stock_file, sheet_name="stock")
