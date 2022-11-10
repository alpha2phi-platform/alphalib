import plotly.graph_objects as go
import plotly.io as pio
import yfinance as yf


def calculate_bb(close):
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


def plot_bollinger_bands(symbol: str, period: str = "1y"):
    assert symbol

    stock = yf.Ticker(symbol)
    df = stock.history(period=period)
    df_close = df[["Close"]]

    sma, lower_band, upper_band, buyers, sellers = calculate_bb(df_close)

    pio.templates.default = "plotly_dark"
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=lower_band.index,
            y=lower_band["Lower"],
            name="Lower Band",
            line_color="rgba(173,204,255,0.2)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=upper_band.index,
            y=upper_band["Upper"],
            name="Upper Band",
            fill="tonexty",
            fillcolor="rgba(173,204,255,0.2)",
            line_color="rgba(173,204,255,0.2)",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_close.index, y=df_close["Close"], name="Price", line_color="#636EFA"
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
    fig.update_xaxes(title="Date", rangeslider_visible=True)
    fig.update_yaxes(title="Price")
    fig.update_layout(
        title_text=f"Volatility Indicator - Bollinger Bands for {symbol.upper()}",
        height=1200,
        width=1800,
        showlegend=True,
    )
    fig.show()
