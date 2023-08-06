from datetime import datetime, timedelta
import logging
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import pandas as pd
import requests
import sentry_sdk

def get_player_stats_data():
    """
    Web Scrape function w/ BS4 that grabs aggregate season stats

    Args:
        None

    Returns:
        DataFrame of Player Aggregate Season stats
    """
    try:
        year_stats = 2022
        url = f"https://www.basketball-reference.com/leagues/NBA_{year_stats}_per_game.html"
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")

        headers = [th.getText() for th in soup.findAll("tr", limit=2)[0].findAll("th")]
        headers = headers[1:]

        rows = soup.findAll("tr")[1:]
        player_stats = [
            [td.getText() for td in rows[i].findAll("td")] for i in range(len(rows))
        ]

        stats = pd.DataFrame(player_stats, columns=headers)
        logging.info(
            f"General Stats Extraction Function Successful, retrieving {len(stats)} updated rows"
        )
        return stats
    except BaseException as error:
        logging.error(f"General Stats Extraction Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df


def get_player_stats_transformed(df: pd.DataFrame) -> pd.DataFrame:
    """
    Web Scrape function w/ BS4 that transforms aggregate player season stats.  Player names get accents removed.

    Args:
        df (DataFrame): Raw Data Frame for Player Stats

    Returns:
        DataFrame of Player Aggregate Season stats
    """
    try:
        df["PTS"] = pd.to_numeric(df["PTS"])
        df = df.query("Player == Player").reset_index()
        df["Player"] = (
            df["Player"]
            .str.normalize("NFKD")
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )
        df.columns = df.columns.str.lower()
        df["scrape_date"] = datetime.now().date()
        df = df.drop("index", axis=1)
        logging.info(
            f"General Stats Transformation Function Successful, retrieving {len(df)} updated rows"
        )
        return df
    except BaseException as error:
        logging.error(f"General Stats Transformation Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df
