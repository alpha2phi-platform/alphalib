import os

__version__ = "0.0.1"

COUNTRY: str = "united states"

# Table names from env variables
STOCKS_TABLE_NAME = os.getenv("STOCKS_TABLE")
COUNTRIES_TABLE_NAME = os.getenv("COUNTRIES_TABLE")
STOCKS_INFO_TABLE_NAME = os.getenv("STOCKS_INFO_TABLE")
STOCKS_DIVIDENDS_TABLE_NAME = os.getenv("STOCKS_DIVIDENDS_TABLE")
