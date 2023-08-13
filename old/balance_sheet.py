from dataclasses import dataclass

from yahooquery import Ticker

from alphalib.utils.logging import logger


@dataclass(kw_only=True)
class BalanceSheetAnalysis:
    pass


def balance_sheet_analysis(symbol: str) -> BalanceSheetAnalysis:
    ticker = Ticker(symbol)
    try:
        balance_sheet = ticker.balance_sheet(frequency="q")
        if not balance_sheet.empty:
            print(balance_sheet.T.head(1000000))
            return BalanceSheetAnalysis()
    except Exception:
        logger.error(f"Unable to retrieve balance sheet for {symbol}")
    finally:
        ticker.session.close()
    return BalanceSheetAnalysis()
