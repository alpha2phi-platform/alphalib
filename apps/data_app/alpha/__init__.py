import logging
import numpy as np
import pandas as pd
import asyncio
from yahooquery import Ticker
from streamlit.logger import get_logger

PORTFOLIO_FILE = "data/portfolio.xlsx"
SHEET_NAME_US_MARKET = "us"

LOGGER = get_logger(__name__)


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


def get_stocks(symbols) -> pd.DataFrame:
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


async def get_symbols(symbols: list[str]) -> pd.DataFrame:
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, get_stocks, symbols)
    return data


def show_indicator(row: pd.Series) -> str:
    if row["current_price"] >= row["target_sell_price"]:
        return "SELL"
    if pd.isna(row["unit"]) or row["unit"] <= 1:
        return "MONITOR"
    return "HOLD"


def calculate_price_target(portfolio: pd.DataFrame, stats: pd.DataFrame):
    conditions = [
        (~pd.isna(portfolio["buy_price"]))
        & (portfolio["buy_price"] < portfolio["current_price"])
    ]
    values = [stats["targetLowPrice"]]
    portfolio["target_buy_price"] = np.select(conditions, values)


def get_portfolio() -> pd.DataFrame:
    portfolio = pd.read_excel(PORTFOLIO_FILE)
    symbols = portfolio["symbol"].to_list()

    loop = asyncio.new_event_loop()
    stats = loop.run_until_complete(get_symbols(symbols))
    loop.close()

    portfolio["name"] = stats["shortName"]
    portfolio["buy_value"] = portfolio["unit"] * portfolio["buy_price"]
    portfolio["current_price"] = stats["currentPrice"]
    portfolio["current_value"] = stats["currentPrice"] * portfolio["unit"]
    portfolio["target_sell_price"] = (portfolio["buy_price"] * 1.15).round(decimals=2)
    calculate_price_target(portfolio, stats)
    portfolio["indicator"] = portfolio.apply(show_indicator, axis=1)
    return portfolio


def save_portfolio(df: pd.DataFrame, sheet_name=SHEET_NAME_US_MARKET):
    df.to_excel(PORTFOLIO_FILE, index=False, sheet_name=sheet_name)
