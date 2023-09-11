import pandas as pd
import streamlit as st
from streamlit.logger import get_logger

from alphalib.analysis.dividend import dividend_analysis
from alphalib.analysis.sentiment import finwiz_score
from alphalib.tracker import load_portfolio, save_portfolio
from alphalib.utils.dateutils import month_from
from alphalib.analysis.ta.trend.ichimoku import plot_ichimoku

st.set_page_config(
    page_title="Stock Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📈",
)

LOGGER = get_logger(__name__)


def footer():
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: visible;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def sidebar():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "Alphalib";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sentiment_score(symbol: str) -> (pd.DataFrame, float):
    try:
        df_score = finwiz_score(symbol)
        past_x_months = month_from(-4)
        mean_score = df_score[df_score["date"] >= past_x_months.date()][
            "compound"
        ].mean()
        return df_score, round(mean_score, 4)
    except Exception as e:
        LOGGER.error("Unable to retrieve sentiment score", e)
        return pd.DataFrame(), 0


def update_porfolio(
    portfolio: pd.DataFrame,
    symbol: str,
    input_unit: str,
    input_target_buy_price: str,
    input_buy_price: str,
) -> bool:
    try:
        portfolio.loc[portfolio["symbol"] == symbol, "unit"] = input_unit
        portfolio.loc[
            portfolio["symbol"] == symbol, "target_buy_price"
        ] = input_target_buy_price
        portfolio.loc[portfolio["symbol"] == symbol, "buy_price"] = input_buy_price
        save_portfolio(portfolio)
        return True
    except Exception:
        return False


def content():
    st.title("Stock Analysis")
    portfolio = load_portfolio()
    portfolio["long_name"] = portfolio["symbol"] + "-" + portfolio["name"]
    with st.container():
        option_stock = st.selectbox(
            "Stock", portfolio["long_name"], label_visibility="hidden"
        )
        if option_stock:
            symbol: str = option_stock.split("-")[0]
            analysis = dividend_analysis(symbol)
            stock_details = portfolio[portfolio["symbol"].isin([symbol])]
            with st.form("dividend_form"):
                col1, col2 = st.columns([2, 2])
                with col1:
                    unit = stock_details["unit"].iloc[0]
                    input_unit = st.text_input(
                        "Unit",
                        placeholder="Enter Unit",
                        value=unit,
                    )
                    target_buy_price = stock_details["target_buy_price"].iloc[0]
                    input_target_buy_price = st.text_input(
                        "Target Buy Price",
                        placeholder="Enter Target Buy Price",
                        value=target_buy_price,
                    )
                    buy_price = stock_details["buy_price"].iloc[0]
                    input_buy_price = st.text_input(
                        "Buy Price",
                        placeholder="Enter Buy Price",
                        value=buy_price,
                    )
                with col2:
                    current_price = stock_details["current_price"].iloc[0]
                    st.text(f"Current Price: {current_price}")
                    current_fifty_two_week_low = stock_details["52_weeks_low"].iloc[0]
                    st.text(f"Fifty Two Week Low: {current_fifty_two_week_low}")
                    if st.form_submit_button("Update", use_container_width=True):
                        if update_porfolio(
                            portfolio,
                            symbol,
                            input_unit,
                            input_target_buy_price,
                            input_buy_price,
                        ):
                            st.write(f"Updated the portfolio for {symbol}")
                        else:
                            st.write(f"Unable to update the portfolio for {symbol}")

            st.header(f"{analysis.symbol} - {analysis.interval} Dividend")
            sentiment_analysis, sentiment_mean_score = sentiment_score(symbol)

            tab1, tab2, tab3, tab4 = st.tabs(
                ["Dividend", "Sentiment", "Technical", "Machine Learning"]
            )
            with tab1:
                col1, col2 = st.columns([3, 7])
                with col1:
                    st.text(f"Dividiend Yield: {analysis.dividend_yield_pct}")
                    st.text(f"Annual Dividend: {analysis.annual_dividend}")
                    st.text(f"PE Ratio: {analysis.pe_ratio}")
                    st.text(f"Ex Dividend Date: {analysis.ex_dividend_date}")

                with col2:
                    st.subheader("Dividend vs Prices")
                    st.dataframe(
                        analysis.result, use_container_width=True, hide_index=True
                    )

                st.subheader("Dividend History")
                st.dataframe(
                    analysis.dividend_history,
                    use_container_width=True,
                    hide_index=True,
                )

            with tab2:
                st.subheader("Sentiment Score")
                st.text(f"Sentiment Score: {sentiment_mean_score}")
                st.dataframe(
                    sentiment_analysis, use_container_width=True, hide_index=True
                )

            with tab3:
                st.subheader("Technical Analysis - Ichimoku")
                st.plotly_chart(
                    plot_ichimoku(symbol, show=False).to_dict(),
                    use_container_width=True,
                )

            with tab4:
                st.text(
                    "Machine learning - timeseries using Prophet with seasonality - TODO"
                )


def app():
    sidebar()
    content()
    footer()


if __name__ == "__main__":
    app()
