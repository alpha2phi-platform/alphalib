import asyncio
import time

import numpy as np
import pandas as pd
import streamlit as st
from streamlit.elements.widgets.data_editor import EditableData
from streamlit.logger import get_logger
from yahooquery import Ticker

from alphalib.utils.convertutils import join_dicts
from alphalib.utils.dateutils import days_interval_from_now, from_isoformat

PORTFOLIO_FILE = "data/portfolio.xlsx"
SHEET_NAME_US_MARKET = "us"

LOGGER = get_logger(__name__)


def create_missing_cols(df, target_cols):
    columns = df.columns.tolist()
    missing_cols = list(set(target_cols) - set(columns))
    if len(missing_cols) > 0:
        df[missing_cols] = None


def get_stocks(symbols) -> pd.DataFrame:
    df_symbols = pd.DataFrame()
    fld_list = []
    counter = 0
    for symbol in symbols:
        LOGGER.info(f"Processing {symbol}")
        result: dict = {}
        counter = counter + 1
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
                # Additional columns
                if "fiveYearAvgDividendYield" not in fld_list:
                    fld_list.extend(["fiveYearAvgDividendYield"])
                fld_list.sort()
            create_missing_cols(df_symbol, fld_list)
            df_symbols = pd.concat([df_symbols, df_symbol[fld_list]], ignore_index=True)
        ticker.session.close()
        if counter % 40 == 0:
            LOGGER.info("Processed {} stocks".format(counter))
            time.sleep(5)
    return df_symbols


async def get_symbols(symbols: list[str]) -> pd.DataFrame:
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, get_stocks, symbols)
    return data


def derive_monitor_status(row: pd.Series) -> str:
    if row["ex_dividend_date"]:
        delta = days_interval_from_now(from_isoformat(row["ex_dividend_date"]))
        if delta >= 0 and delta <= 30:
            return "MONITOR - PRE"
        if delta < 0 and delta >= -30:
            return "MONITOR - POST"
    return "MONITOR"


def show_indicator(row: pd.Series) -> str:
    if row["current_price"] >= row["target_sell_price"] and row["unit"] > 0:
        return "SELL"
    # if pd.isna(row["unit"]) or row["unit"] == 0:
    #     return derive_monitor_status(row)
    if row["current_price"] <= row["target_buy_price"] * 1.03:
        if row["current_price"] <= round(row["52_weeks_low"] * 1.01, 2):
            return "BUY BUY"
        else:
            return "BUY"
    return derive_monitor_status(row)


def calculate_price_target(portfolio: pd.DataFrame, stats: pd.DataFrame):
    # portfolio["target_buy_price"] = np.where(
    #     ~pd.isna(portfolio["buy_price"]) & portfolio["buy_price"] > 0,
    #     portfolio["buy_price"],
    #     stats["fiftyTwoWeekLow"] * 1.01,
    # )
    portfolio["target_buy_price"] = round(stats["fiftyTwoWeekLow"] * 1.02, 2)
    conditions = [
        (~pd.isna(portfolio["buy_price"]))
        & (portfolio["buy_price"] > 0)
        & (portfolio["buy_price"] < portfolio["target_buy_price"])
    ]
    values = [portfolio["buy_price"]]
    portfolio["target_buy_price"] = np.select(
        conditions, values, portfolio["target_buy_price"]
    )


def load_portfolio() -> EditableData | pd.DataFrame:
    if "portfolio" in st.session_state:
        return st.session_state.portfolio
    else:
        return pd.read_excel(PORTFOLIO_FILE)


def refresh_porfolio(portfolio):
    symbols = portfolio["symbol"].to_list()
    loop = asyncio.new_event_loop()
    stats = loop.run_until_complete(get_symbols(symbols))
    loop.close()

    TARGET_SELL_PCT = 1.10

    portfolio["name"] = stats["shortName"]
    portfolio["buy_value"] = portfolio["unit"] * portfolio["buy_price"]
    portfolio["current_price"] = stats["currentPrice"]
    portfolio["beta"] = stats["beta"]
    portfolio["dividend_yield"] = stats["dividendYield"]
    portfolio["five_year_avg_dividend_yield"] = stats.get(
        "fiveYearAvgDividendYield", None
    )
    portfolio["52_weeks_low"] = stats["fiftyTwoWeekLow"]
    portfolio["52_weeks_high"] = stats["fiftyTwoWeekHigh"]
    portfolio["ex_dividend_date"] = stats["exDividendDate"]
    portfolio["current_value"] = stats["currentPrice"] * portfolio["unit"]
    portfolio["target_sell_price"] = (portfolio["buy_price"] * TARGET_SELL_PCT).round(
        decimals=2
    )
    # calculate_price_target(portfolio, stats)
    portfolio["indicator"] = portfolio.apply(show_indicator, axis=1)
    portfolio["nasdaq_url"] = portfolio["symbol"].apply(
        lambda x: f"https://www.nasdaq.com/market-activity/stocks/{x.lower()}/dividend-history"
    )
    portfolio["yahoo_finance_url"] = portfolio["symbol"].apply(
        lambda x: f"https://finance.yahoo.com/quote/{x}?p={x}"
    )
    portfolio["earnings_date"] = stats["earnings"]


def save_portfolio(df: pd.DataFrame, sheet_name=SHEET_NAME_US_MARKET):
    df.to_excel(PORTFOLIO_FILE, index=False, sheet_name=sheet_name)
