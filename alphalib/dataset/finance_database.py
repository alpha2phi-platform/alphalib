from typing import Literal

import financedatabase as fd
import pandas as pd
from sqlalchemy import create_engine


def prepare_stock_dataset(
    save: bool = False, format: Literal["excel", "sqlite"] = "excel"
) -> pd.DataFrame:
    equities = fd.Equities()
    all_equities = equities.select()
    df_all_equities = pd.DataFrame(all_equities)
    df_all_equities.reset_index(inplace=True)
    if save:
        if format == "sqlite":
            engine = create_engine("sqlite://stock.db")
            df_all_equities.to_sql("stock", con=engine, if_exists="replace")
        else:
            df_all_equities.to_excel(
                "stock.xlsx",
                index=False,
                header=True,
                engine="openpyxl",
                sheet_name="stock",
            )
    return df_all_equities
