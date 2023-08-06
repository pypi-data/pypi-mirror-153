import os
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import logging
import pandas as pd
import requests
import sentry_sdk

from .utils import clean_player_names

def get_shooting_stats_data():
    """
    Web Scrape function w/ pandas read_html that grabs all raw shooting stats

    Args:
        None

    Returns:
        DataFrame of raw shooting stats
    """
    try:
        url = "https://www.basketball-reference.com/leagues/NBA_2022_shooting.html"
        df = pd.read_html(url)[0]
        logging.info(
            f"Shooting Stats Web Scrape Function Successful, retrieving {len(df)} rows for Shooting Stats"
        )
        return df
    except BaseException as error:
        logging.error(f"Shooting Stats Web Scrape Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df


def get_shooting_stats_transformed(df: pd.DataFrame) -> pd.DataFrame:
    """
    Web Scrape Transformation function for Shooting Stats.
    This has some multi index bullshit attached in the beginning if it screws up the future - that's probably it.

    Args:
        df (DataFrame): The Raw Shooting Stats DF

    Returns:
        DataFrame of Transformed Shooting Stats
    """
    try:
        df.columns = df.columns.to_flat_index()
        df = df.rename(
            columns={
                df.columns[1]: "player",
                df.columns[6]: "mp",
                df.columns[8]: "avg_shot_distance",
                df.columns[10]: "pct_fga_2p",
                df.columns[11]: "pct_fga_0_3",
                df.columns[12]: "pct_fga_3_10",
                df.columns[13]: "pct_fga_10_16",
                df.columns[14]: "pct_fga_16_3p",
                df.columns[15]: "pct_fga_3p",
                df.columns[18]: "fg_pct_0_3",
                df.columns[19]: "fg_pct_3_10",
                df.columns[20]: "fg_pct_10_16",
                df.columns[21]: "fg_pct_16_3p",
                df.columns[24]: "pct_2pfg_ast",
                df.columns[25]: "pct_3pfg_ast",
                df.columns[27]: "dunk_pct_tot_fg",
                df.columns[28]: "dunks",
                df.columns[30]: "corner_3_ast_pct",
                df.columns[31]: "corner_3pm_pct",
                df.columns[33]: "heaves_att",
                df.columns[34]: "heaves_makes",
            }
        )[
            [
                "player",
                "mp",
                "avg_shot_distance",
                "pct_fga_2p",
                "pct_fga_0_3",
                "pct_fga_3_10",
                "pct_fga_10_16",
                "pct_fga_16_3p",
                "pct_fga_3p",
                "fg_pct_0_3",
                "fg_pct_3_10",
                "fg_pct_10_16",
                "fg_pct_16_3p",
                "pct_2pfg_ast",
                "pct_3pfg_ast",
                "dunk_pct_tot_fg",
                "dunks",
                "corner_3_ast_pct",
                "corner_3pm_pct",
                "heaves_att",
                "heaves_makes",
            ]
        ]
        df = df.query('player != "Player"').copy()
        df["mp"] = pd.to_numeric(df["mp"])
        df = (
            df.sort_values(["mp"], ascending=False)
            .groupby("player")
            .first()
            .reset_index()
            .drop("mp", axis=1)
        )
        df["player"] = (
            df["player"]
            .str.normalize("NFKD")  # this is removing all accented characters
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )
        df = clean_player_names(df)
        df["scrape_date"] = datetime.now().date()
        df["scrape_ts"] = datetime.now()
        logging.info(
            f"Shooting Stats Transformation Function Successful, retrieving {len(df)} rows"
        )
        return df
    except BaseException as e:
        logging.error(f"Shooting Stats Transformation Function Failed, {e}")
        sentry_sdk.capture_exception(e)
        df = []
        return df
