import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf


def plot_bb(symbol: str):
    assert symbol

    stock = yf.Ticker(symbol)
    data = stock.history(period="1y")
    df_close = data[["Close"]]

    sma = df_close.rolling(window=20).mean().dropna()
    rstd = df_close.rolling(window=20).std().dropna()

    upper_band = sma + 2 * rstd
    lower_band = sma - 2 * rstd

    upper_band = upper_band.rename(columns={"Close": "upper"})
    lower_band = lower_band.rename(columns={"Close": "lower"})
    bb = df_close.join(upper_band).join(lower_band)
    bb = bb.dropna()

    buyers = bb[bb["Close"] <= bb["lower"]]
    sellers = bb[bb["Close"] >= bb["upper"]]

    # Plotting
    pio.templates.default = "plotly_dark"

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=lower_band.index,
            y=lower_band["lower"],
            name="Lower Band",
            line_color="rgba(173,204,255,0.2)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=upper_band.index,
            y=upper_band["upper"],
            name="Upper Band",
            fill="tonexty",
            fillcolor="rgba(173,204,255,0.2)",
            line_color="rgba(173,204,255,0.2)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_close.index, y=df_close["Close"], name="Close", line_color="#636EFA"
        )
    )
    fig.add_trace(
        go.Scatter(x=sma.index, y=sma["Close"], name="SMA", line_color="#FECB52")
    )
    fig.add_trace(
        go.Scatter(
            x=buyers.index,
            y=buyers["Close"],
            name="Buyers",
            mode="markers",
            marker=dict(
                color="#00CC96",
                size=10,
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=sellers.index,
            y=sellers["Close"],
            name="Sellers",
            mode="markers",
            marker=dict(
                color="#EF553B",
                size=10,
            ),
        )
    )
    fig.show()


# Here we will add a middle band (20 days), upper band (20 days + 1.96 std),
# and lower band (20 days - 1.96 std)
def add_bollinger_bands(df):
    df["middle_band"] = df["Close"].rolling(window=20).mean()
    df["upper_band"] = df["middle_band"] + 1.96 * df["Close"].rolling(window=20).std()
    df["lower_band"] = df["middle_band"] - 1.96 * df["Close"].rolling(window=20).std()
    # df.to_csv(PATH + ticker + '.csv')
    return df


def plot_bb2(symbol: str):
    assert symbol

    fig = go.Figure()
    stock = yf.Ticker(symbol)
    df = stock.history(period="1y")
    df = add_bollinger_bands(df)

    candle = go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Candlestick",
    )

    upper_line = go.Scatter(
        x=df.index,
        y=df["upper_band"],
        line=dict(color="rgba(250, 0, 0, 0.75)", width=1),
        name="Upper Band",
    )

    mid_line = go.Scatter(
        x=df.index,
        y=df["middle_band"],
        line=dict(color="rgba(0, 0, 250, 0.75)", width=0.7),
        name="Middle Band",
    )

    lower_line = go.Scatter(
        x=df.index,
        y=df["lower_band"],
        line=dict(color="rgba(0, 250, 0, 0.75)", width=1),
        name="Lower Band",
    )

    fig.add_trace(candle)
    fig.add_trace(upper_line)
    fig.add_trace(mid_line)
    fig.add_trace(lower_line)

    fig.update_xaxes(title="Date", rangeslider_visible=True)
    fig.update_yaxes(title="Price")

    # USED FOR NON-DAILY DATA : Get rid of empty dates and market closed
    # fig.update_layout(title=ticker + " Bollinger Bands",
    # height=1200, width=1800,
    #               showlegend=True,
    #               xaxis_rangebreaks=[
    #         dict(bounds=["sat", "mon"]),
    #         dict(bounds=[16, 9.5], pattern="hour"),
    #         dict(values=["2021-12-25", "2022-01-01"])
    #     ])

    fig.update_layout(
        title=symbol + " Bollinger Bands", height=1200, width=1800, showlegend=True
    )
    fig.show()
