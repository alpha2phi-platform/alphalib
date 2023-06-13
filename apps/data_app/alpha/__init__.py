import pandas as pd
import asyncio
from yahooquery import Ticker

PORTFOLIO_FILE = "data/portfolio.xlsx"


def create_missing_cols(df, target_cols):
    columns = df.columns.tolist()
    missing_cols = list(set(target_cols) - set(columns))
    if len(missing_cols) > 0:
        df[missing_cols] = None


def join_dicts(to_dict, from_dict, from_dict_key=None) -> dict:
    v = from_dict
    if from_dict_key in from_dict:
        v = from_dict[from_dict_key]

    if type(v) is dict:
        to_dict = {**to_dict, **v}
    return to_dict


def get_portfolio() -> pd.DataFrame:
    return pd.read_excel(PORTFOLIO_FILE)


def save_portfolio(df: pd.DataFrame):
    df.to_excel(PORTFOLIO_FILE, index=False)


def get_stocks(symbols) -> pd.DataFrame:
    symbols = ["AAPL", "EFC", "OXLC"]
    df_symbols = pd.DataFrame()
    fld_list = []
    for symbol in symbols:
        result: dict = {}
        ticker = Ticker(symbol)
        key_stats = ticker.key_stats
        result = join_dicts(result, key_stats, symbol)
        result = join_dicts(result, ticker.quote_type, symbol)
        result = join_dicts(result, ticker.summary_detail, symbol)
        result = join_dicts(result, ticker.summary_profile, symbol)
        result = join_dicts(result, ticker.calendar_events, symbol)
        result = join_dicts(result, ticker.financial_data, symbol)
        result = join_dicts(result, ticker.price, symbol)
        df_symbol = pd.DataFrame([result])
        if len(df_symbol) > 0 and len(df_symbol.columns) > 0:
            if len(fld_list) == 0:
                fld_list.extend(df_symbol.columns.tolist())
                fld_list.sort()
            create_missing_cols(df_symbol, fld_list)
            df_symbols = pd.concat([df_symbols, df_symbol[fld_list]], ignore_index=True)
        ticker.session.close()
    return df_symbols
