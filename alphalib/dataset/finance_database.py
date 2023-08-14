import pandas as pd
import financedatabase as fd


def prepare_stock_dataset(save_to_excel: bool = False) -> pd.DataFrame:
    equities = fd.Equities()
    all_equities = equities.select()
    df_all_equities = pd.DataFrame(all_equities)
    df_all_equities.reset_index(inplace=True)
    if save_to_excel:
        df_all_equities.to_excel(
            "stock.xlsx",
            index=False,
            header=True,
            engine="openpyxl",
            sheet_name="stock",
        )
    return df_all_equities
