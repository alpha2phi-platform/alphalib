import pandas as pd
import streamlit as st
from streamlit.logger import get_logger

from alphalib.analysis.dividend import dividend_analysis
from alphalib.analysis.sentiment import finwiz_score
from alphalib.tracker import get_portfolio
from alphalib.utils.dateutils import month_from
from alphalib.analysis.ta.trend.ichimoku import plot_ichimoku

st.set_page_config(
    page_title="Dividend Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="💰",
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
    df_score = finwiz_score(symbol)
    past_x_months = month_from(-4)
    mean_score = df_score[df_score["date"] >= past_x_months.date()]["compound"].mean()
    return df_score, round(mean_score, 4)


def content():
    st.title("Dividend Analysis")
    portfolio = get_portfolio()
    portfolio["long_name"] = portfolio["symbol"] + "-" + portfolio["name"]
    with st.container():
        option = st.selectbox(
            "Stock", portfolio["long_name"], label_visibility="hidden"
        )
        if option:
            symbol = option.split("-")[0]
            analysis = dividend_analysis(symbol)

            st.header(f"{analysis.symbol} - {analysis.interval} Dividend")
            sentiment_analysis, sentiment_mean_score = sentiment_score(symbol)

            tab1, tab2, tab3 = st.tabs(
                ["Dividend Analysis", "Sentiment Analysis", "Technical Analysis"]
            )
            with tab1:
                col1, col2 = st.columns([2, 4])
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
                    analysis.dividend_history, use_container_width=True, hide_index=True
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


def app():
    sidebar()
    content()
    footer()


if __name__ == "__main__":
    app()
