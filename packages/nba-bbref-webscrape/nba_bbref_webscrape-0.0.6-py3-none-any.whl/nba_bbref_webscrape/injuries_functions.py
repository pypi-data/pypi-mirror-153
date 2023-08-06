import os
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import logging
import pandas as pd
import requests
import sentry_sdk

from .utils import clean_player_names

def get_injuries_data():
    """
    Web Scrape function w/ pandas read_html that grabs all current injuries

    Args:
        None

    Returns:
        Pandas DataFrame of all current player injuries & their associated team
    """
    try:
        url = "https://www.basketball-reference.com/friv/injuries.fcgi"
        df = pd.read_html(url)[0]
        logging.info(
            f"Injury Web Scrape Function Successful, retrieving {len(df)} rows"
        )
        return df
    except BaseException as error:
        logging.error(f"Injury Web Scrape Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df


def get_injuries_transformed(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformation Function for injuries function

    Args:
        df (DataFrame): Raw Injuries DataFrame

    Returns:
        Pandas DataFrame of all current player injuries & their associated team
    """
    try:
        df = df.rename(columns={"Update": "Date"})
        df.columns = df.columns.str.lower()
        df["scrape_date"] = datetime.now().date()
        df["player"] = (
            df["player"]
            .str.normalize("NFKD")  # this is removing all accented characters
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )
        df = clean_player_names(df)
        logging.info(
            f"Injury Transformation Function Successful, retrieving {len(df)} rows"
        )
        return df
    except BaseException as error:
        logging.error(f"Injury Transformation Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df
