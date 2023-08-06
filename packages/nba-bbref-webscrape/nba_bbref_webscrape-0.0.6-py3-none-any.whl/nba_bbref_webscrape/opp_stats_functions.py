import os
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import logging
import pandas as pd
import requests
import sentry_sdk

from .utils import clean_player_names

day = (datetime.now() - timedelta(1)).day
month = (datetime.now() - timedelta(1)).month
year = (datetime.now() - timedelta(1)).year

def get_opp_stats_data():
    """
    Web Scrape function w/ pandas read_html that grabs all regular season opponent team stats

    Args:
        None

    Returns:
        Pandas DataFrame of all current team opponent stats
    """
    try:
        url = "https://www.basketball-reference.com/leagues/NBA_2022.html"
        df = pd.read_html(url)[5]
        logging.info(
            f"Opp Stats Web Scrape Function Successful, retrieving {len(df)} rows for {year}-{month}-{day}"
        )
        return df
    except BaseException as error:
        logging.error(f"Opp Stats Web Scrape Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df


def get_opp_stats_transformed(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformation Function for Opponent Stats.

    Args:
        df (DataFrame): The Raw Opponent Stats DataFrame

    Returns:
        DataFrame of transformed Opponent Stats Data
    """
    try:
        df = df[["Team", "FG%", "3P%", "3P", "PTS"]]
        df = df.rename(
            columns={
                df.columns[0]: "team",
                df.columns[1]: "fg_percent_opp",
                df.columns[2]: "threep_percent_opp",
                df.columns[3]: "threep_made_opp",
                df.columns[4]: "ppg_opp",
            }
        )
        df = df.query('team != "League Average"')
        df = df.reset_index(drop=True)
        df["scrape_date"] = datetime.now().date()
        logging.info(
            f"Opp Stats Transformation Function Successful, retrieving {len(df)} rows for {year}-{month}-{day}"
        )
        return df
    except BaseException as error:
        logging.error(f"Opp Stats Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df