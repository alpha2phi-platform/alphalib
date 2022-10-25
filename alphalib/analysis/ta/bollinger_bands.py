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
