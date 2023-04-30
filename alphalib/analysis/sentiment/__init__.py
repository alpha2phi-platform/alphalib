from contextlib import closing

import nltk
import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from requests.adapters import HTTPAdapter

from alphalib.utils.httputils import (
    DEFAULT_HTTP_RETRY,
    DEFAULT_HTTP_TIMEOUT,
    http_headers,
)

FINWIZ_URL = "https://finviz.com/quote.ashx?t="

# Download corpus
nltk.download("vader_lexicon", quiet=True)


def sentiment_analysis(symbol: str) -> pd.DataFrame:
    assert symbol

    news_tables = {}
    url = FINWIZ_URL + symbol
    with closing(requests.Session()) as s:
        s.verify = False
        s.mount("https://", HTTPAdapter(max_retries=DEFAULT_HTTP_RETRY))
        r = s.get(
            url, verify=True, headers=http_headers(), timeout=DEFAULT_HTTP_TIMEOUT
        )
        if r.status_code != requests.status_codes.codes["ok"]:
            raise ConnectionError(
                "ERR: error " + str(r.status_code) + ", try again later."
            )
        soup = BeautifulSoup(r.text, "lxml")
        news_table: Tag = soup.select_one("#news-table")
        news_tables[symbol] = news_table

        parsed_news = []
        for file_name, news_table in news_tables.items():
            for x in news_table.find_all("tr"):
                text = x.a.get_text()
                date_scrape = x.td.text.split()
                if len(date_scrape) == 1:
                    time = date_scrape[0]
                else:
                    date = date_scrape[0]
                    time = date_scrape[1]
                ticker = file_name.split("_")[0]

                parsed_news.append([ticker, date, time, text])

        vader = SentimentIntensityAnalyzer()
        columns = ["ticker", "date", "time", "headline"]
        parsed_and_scored_news = pd.DataFrame(parsed_news, columns=columns)
        # print(parsed_and_scored_news.T.head(1))
        scores = (
            parsed_and_scored_news["headline"].apply(vader.polarity_scores).tolist()
        )
        scores_df = pd.DataFrame(scores)
        parsed_and_scored_news = parsed_and_scored_news.join(
            scores_df, rsuffix="_right"
        )
        parsed_and_scored_news["date"] = pd.to_datetime(
            parsed_and_scored_news.date, format="%b-%d-%y"
        ).dt.date

        return parsed_and_scored_news

        # plt.rcParams["figure.figsize"] = [10, 6]
        # mean_scores = parsed_and_scored_news.groupby(["ticker", "date"]).mean()
        # mean_scores = mean_scores.unstack()
        # mean_scores = mean_scores.xs("compound", axis="columns").transpose()
        # mean_scores.plot(kind="bar")
        # plt.grid()
