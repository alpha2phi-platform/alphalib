import json
import re
import time
from decimal import Decimal

import boto3
import investpy
import pandas as pd

from .. import COUNTRIES_TABLE_NAME, STOCKS_TABLE_NAME
from ..utils import current_time_utc, logger, to_epoch_time, to_isoformat


def get_stock_countries() -> list[str]:
    """Get stock countries

    Get supported countries.

    Returns:
        list[str]: A list of countries.
    """
    return investpy.stocks.get_stock_countries()


def get_stocks(country: str) -> pd.DataFrame:
    return investpy.stocks.get_stocks(country)


def get_stock_info(country, symbol) -> pd.DataFrame:
    try:
        stock_info = investpy.get_stock_information(symbol, country)
        stock_info["country"] = country
        return stock_info
    except Exception as e:
        logger.exception(f"Error getting stock for {country} - {symbol}", e)
        return pd.DataFrame()


def get_stock_dividends(symbol, country) -> pd.DataFrame:
    try:
        return investpy.get_stock_dividends(symbol, country)
    except Exception as e:
        logger.exception(f"Error getting stock for {country} - {symbol}", e)
        return pd.DataFrame()


def get_all_stocks_info(stocks):
    stocks_info = None
    count = 0
    for _, row in stocks.iterrows():
        count = count + 1
        stock = get_stock_info(row.symbol, row.country)
        if stock is None:
            continue
        if stocks_info is None:
            stocks_info = stock
        else:
            stocks_info = stocks_info.append(stock)
        if count % 10 == 0:
            print(f"Saving {count}/{len(stocks)}")
            # TODO
            # save_csv(df_stocks_info, STOCKS_INFO_DATASET)
            time.sleep(3)
    # TODO
    # save_csv(df_stocks_info, STOCKS_INFO_DATASET)


def get_stocks_dividends(df):
    stocks_dividends = None
    count = 0
    for _, row in df.iterrows():
        count = count + 1
        # print(f"{count}/{len(df)}: {row.symbol}-{row['name']}")
        stock = get_stock_dividends(row.symbol, row.country)
        if stock is None:
            continue
        stock["Symbol"] = row.symbol
        if stocks_dividends is None:
            stocks_dividends = stock
        else:
            stocks_dividends = stocks_dividends.append(stock)
        if count % 10 == 0:
            print(f"Saving {count}/{len(df)}")
            # TODO
            # save_csv(df_stocks_dividends, STOCKS_DIVIDENDS_DATASET)
            time.sleep(3)
    # TODO
    # save_csv(df_stocks_dividends, STOCKS_DIVIDENDS_DATASET)


def sanitized_column_name(name):
    if not name:
        raise ValueError("Name cannot be empty")
    name = re.sub(r"[\s().\-/]+", "_", name.lower())
    name = re.sub(r"(^\d)", r"_\1", name)
    name = name.removesuffix("_")
    return name


def update_countries(countries):
    dynamodb = boto3.resource("dynamodb")
    countries_table = dynamodb.Table(COUNTRIES_TABLE_NAME)
    with countries_table.batch_writer() as batch:
        for country in countries:
            item = {"country": country}
            batch.put_item(Item=item)


def update_stocks(stocks):
    dynamodb = boto3.resource("dynamodb")
    stocks_table = dynamodb.Table(STOCKS_TABLE_NAME)

    # Add timestamp fields
    now = current_time_utc()
    stocks["update_datetime_isoformat"] = to_isoformat(now)
    stocks["update_datetime"] = to_epoch_time(now)
    # Not required
    # stocks["info_update_datetime_isoformat"] = None
    # stocks["info_update_datetime"] = None

    with stocks_table.batch_writer() as batch:
        for _, row in stocks.iterrows():
            batch.put_item(json.loads(row.to_json(), parse_float=Decimal))


# stocks.apply(update_stock, axis=1)

# def update_stock(row):
#     """Update stock table
#
#     Args:
#         row : Stock.
#     """
#     item = {
#         "country": row[0],
#         "symbol": row[5],
#         "name": row[1],
#         "full_name": row[2],
#         "isin": row[3],
#         "currency": row[4],
#     }
#     print(item)
#     stocks_table.put_item(Item=item)
