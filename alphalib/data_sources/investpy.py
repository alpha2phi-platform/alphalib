import investpy
import pandas as pd

from ..utils import logger


def get_stock_countries() -> list[str]:
    """Get stock countries.

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


def get_stock_dividends(country, symbol) -> pd.DataFrame:
    try:
        return investpy.get_stock_dividends(symbol, country)
    except Exception as e:
        logger.exception(f"Error getting stock for {country} - {symbol}", e)
        return pd.DataFrame()


# def get_all_stocks_info(stocks):
#     stocks_info = None
#     count = 0
#     for _, row in stocks.iterrows():
#         count = count + 1
#         stock = get_stock_info(row.symbol, row.country)
#         if stock is None:
#             continue
#         if stocks_info is None:
#             stocks_info = stock
#         else:
#             stocks_info = stocks_info.append(stock)
#         if count % 10 == 0:
#             print(f"Saving {count}/{len(stocks)}")
#             # TODO
#             # save_csv(df_stocks_info, STOCKS_INFO_DATASET)
#             time.sleep(3)
#     # TODO
#     # save_csv(df_stocks_info, STOCKS_INFO_DATASET)


# def get_stocks_dividends(df):
#     stocks_dividends = None
#     count = 0
#     for _, row in df.iterrows():
#         count = count + 1
#         # print(f"{count}/{len(df)}: {row.symbol}-{row['name']}")
#         stock = get_stock_dividends(row.symbol, row.country)
#         if stock is None:
#             continue
#         stock["Symbol"] = row.symbol
#         if stocks_dividends is None:
#             stocks_dividends = stock
#         else:
#             stocks_dividends = stocks_dividends.append(stock)
#         if count % 10 == 0:
#             print(f"Saving {count}/{len(df)}")
#             # TODO
#             # save_csv(df_stocks_dividends, STOCKS_DIVIDENDS_DATASET)
#             time.sleep(3)
#     # TODO
#     # save_csv(df_stocks_dividends, STOCKS_DIVIDENDS_DATASET)
