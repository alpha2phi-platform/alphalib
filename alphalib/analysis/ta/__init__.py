import numpy as np
import pandas as pd


def daily_return(close):
    return (close / close.shift(1)) - 1


def cum_return(daily_return):
    return (1 + daily_return).cumprod()


def volatility_bollinger_bands(close):
    sma = close.rolling(window=20).mean().dropna()
    rstd = close.rolling(window=20).std().dropna()

    upper_band = sma + 2 * rstd
    lower_band = sma - 2 * rstd

    upper_band = upper_band.rename(columns={"Close": "Upper"})
    lower_band = lower_band.rename(columns={"Close": "Lower"})
    bb = close.join(upper_band).join(lower_band)
    bb = bb.dropna()

    buyers = bb[bb["Close"] <= bb["Lower"]]
    sellers = bb[bb["Close"] >= bb["Upper"]]

    return sma, lower_band, upper_band, buyers, sellers


def volatility_atr(high, low, close, n=14):
    tr = np.amax(
        np.vstack(
            (
                (high - low).to_numpy(),
                (abs(high - close)).to_numpy(),
                (abs(low - close)).to_numpy(),
            )
        ).T,
        axis=1,
    )
    return pd.Series(tr).rolling(n).mean().to_numpy()


def trend_ichimoku(high, low, close):
    # Conversion
    hi_val = high.rolling(window=9).max()
    low_val = low.rolling(window=9).min()
    conversion = (hi_val + low_val) / 2

    # Baseline
    hi_val2 = high.rolling(window=26).max()
    low_val2 = low.rolling(window=26).min()
    baseline = (hi_val2 + low_val2) / 2

    # Spans
    span_A = ((conversion + baseline) / 2).shift(26)
    hi_val3 = high.rolling(window=52).max()
    low_val3 = low.rolling(window=52).min()
    span_B = ((hi_val3 + low_val3) / 2).shift(26)
    lagging = close.shift(-26)

    return conversion, baseline, span_A, span_B, lagging


def momentum_rsi(close, periods=14):

    close_delta = close.diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    return rsi
