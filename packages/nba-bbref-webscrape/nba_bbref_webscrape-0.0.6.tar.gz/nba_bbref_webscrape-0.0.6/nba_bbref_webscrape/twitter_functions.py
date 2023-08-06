from datetime import datetime, timedelta
import os

from bs4 import BeautifulSoup
import logging
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
import pandas as pd
import requests
import sentry_sdk
import twint

def scrape_tweets(search_term: str) -> pd.DataFrame:
    """
    Twitter Scrape function using twint to grab between 1,000 and 2,000 tweets about the search parameter.
    It has to like write to a fkn csv then read from csv, idk, thx for the OOP.
    The twint package is no longer updated so probably want to use official Twitter API for this.

    Args:
        search_term (str): The term to search Tweets for.

    Returns:
        DataFrame of around 1-2k Tweets

    
    """
    try:
        c = twint.Config()
        c.Search = search_term
        c.Limit = 2500  # number of Tweets to scrape
        c.Store_csv = True  # store tweets in a csv file
        c.Output = f"{search_term}_tweets.csv"  # path to csv file
        c.Hide_output = True

        twint.run.Search(c)
        df = pd.read_csv(f"{search_term}_tweets.csv")
        df = df[
            [
                "id",
                "created_at",
                "date",
                "username",
                "tweet",
                "language",
                "link",
                "likes_count",
                "retweets_count",
                "replies_count",
            ]
        ].drop_duplicates()
        df["scrape_date"] = datetime.now().date()
        df["scrape_ts"] = datetime.now()
        df = df.query('language=="en"').groupby("id").agg("last")

        analyzer = SentimentIntensityAnalyzer()
        df["compound"] = [analyzer.polarity_scores(x)["compound"] for x in df["tweet"]]
        df["neg"] = [analyzer.polarity_scores(x)["neg"] for x in df["tweet"]]
        df["neu"] = [analyzer.polarity_scores(x)["neu"] for x in df["tweet"]]
        df["pos"] = [analyzer.polarity_scores(x)["pos"] for x in df["tweet"]]
        df["sentiment"] = np.where(df["compound"] > 0, 1, 0)
        logging.info(
            f"Twitter Tweet Extraction Success, retrieving {len(df)} total tweets"
        )
        return df
    except BaseException as e:
        logging.error(f"Twitter Tweet Extraction Failed, {e}")
        sentry_sdk.capture_exception(e)
        df = []
        return df
