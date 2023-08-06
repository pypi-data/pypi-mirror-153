from datetime import datetime, timedelta
import logging
import os
from typing import List

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import numpy as np
import pandas as pd
import praw
import sentry_sdk

today = datetime.now().date()
todaytime = datetime.now()

def get_reddit_data(sub: str) -> pd.DataFrame:
    """
    Web Scrape function w/ PRAW that grabs top ~27 top posts from a given subreddit.
    Left sub as an argument in case I want to scrape multi subreddits in the future (r/nba, r/nbadiscussion, r/sportsbook etc)

    Args:
        sub (string): subreddit to query

    Returns:
        Pandas DataFrame of all current top posts on r/nba
    """
    reddit = praw.Reddit(
        client_id=os.environ.get("reddit_accesskey"),
        client_secret=os.environ.get("reddit_secretkey"),
        user_agent="praw-app",
        username=os.environ.get("reddit_user"),
        password=os.environ.get("reddit_pw"),
    )
    try:
        subreddit = reddit.subreddit(sub)
        posts = []
        for post in subreddit.hot(limit=27):
            posts.append(
                [
                    post.title,
                    post.score,
                    post.id,
                    post.url,
                    str(f"https://www.reddit.com{post.permalink}"),
                    post.num_comments,
                    post.selftext,
                    today,
                    todaytime,
                ]
            )
        posts = pd.DataFrame(
            posts,
            columns=[
                "title",
                "score",
                "id",
                "url",
                "reddit_url",
                "num_comments",
                "body",
                "scrape_date",
                "scrape_time",
            ],
        )
        posts.columns = posts.columns.str.lower()

        logging.info(
            f"Reddit Scrape Successful, grabbing 27 Recent popular posts from r/{sub} subreddit"
        )
        return posts
    except BaseException as error:
        logging.error(f"Reddit Scrape Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        data = []
        return data


def get_reddit_comments(urls: pd.Series) -> pd.DataFrame:
    """
    Web Scrape function w/ PRAW that iteratively extracts comments from provided reddit post urls.

    Args:
        urls (Series): The (reddit) urls to extract comments from

    Returns:
        Pandas DataFrame of all comments from the provided reddit urls
    """
    reddit = praw.Reddit(
        client_id=os.environ.get("reddit_accesskey"),
        client_secret=os.environ.get("reddit_secretkey"),
        user_agent="praw-app",
        username=os.environ.get("reddit_user"),
        password=os.environ.get("reddit_pw"),
    )
    author_list = []
    comment_list = []
    score_list = []
    flair_list1 = []
    flair_list2 = []
    edited_list = []
    url_list = []

    try:
        for i in urls:
            submission = reddit.submission(url=i)
            submission.comments.replace_more(limit=0)
            # this removes all the "more comment" stubs
            # to grab ALL comments use limit=None, but it will take 100x longer
            for comment in submission.comments.list():
                author_list.append(comment.author)
                comment_list.append(comment.body)
                score_list.append(comment.score)
                flair_list1.append(comment.author_flair_css_class)
                flair_list2.append(comment.author_flair_text)
                edited_list.append(comment.edited)
                url_list.append(i)

        df = pd.DataFrame(
            {
                "author": author_list,
                "comment": comment_list,
                "score": score_list,
                "url": url_list,
                "flair1": flair_list1,
                "flair2": flair_list2,
                "edited": edited_list,
                "scrape_date": datetime.now().date(),
                "scrape_ts": datetime.now(),
            }
        )

        df = df.astype({"author": str})
        # adding sentiment analysis columns
        analyzer = SentimentIntensityAnalyzer()
        df["compound"] = [
            analyzer.polarity_scores(x)["compound"] for x in df["comment"]
        ]
        df["neg"] = [analyzer.polarity_scores(x)["neg"] for x in df["comment"]]
        df["neu"] = [analyzer.polarity_scores(x)["neu"] for x in df["comment"]]
        df["pos"] = [analyzer.polarity_scores(x)["pos"] for x in df["comment"]]
        df["sentiment"] = np.where(df["compound"] > 0, 1, 0)

        df["edited"] = np.where(
            df["edited"] == False, 0, 1
        )  # if edited, then 1, else 0
        logging.info(
            f"Reddit Comment Extraction Success, retrieving {len(df)} total comments from {len(urls)} total urls"
        )
        return df
    except BaseException as e:
        logging.error(f"Reddit Comment Extraction Failed for url {i}, {e}")
        sentry_sdk.capture_exception(e)
        df = []
        return df