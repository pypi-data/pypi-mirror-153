from datetime import datetime, timedelta
import logging
import os

import pandas as pd
import requests
import sentry_sdk

def get_advanced_stats_data():
    """
    Web Scrape function w/ pandas read_html that grabs all team advanced stats

    Args:
        None

    Returns:
        DataFrame of all current Team Advanced Stats
    """
    try:
        url = "https://www.basketball-reference.com/leagues/NBA_2022.html"
        df = pd.read_html(url)
        df = pd.DataFrame(df[10])
        logging.info(
            f"Advanced Stats Web Scrape Function Successful, retrieving updated data for 30 Teams"
        )
        return df
    except BaseException as error:
        logging.error(f"Advanced Stats Web Scrape Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df


def get_advanced_stats_transformed(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformation function for Advanced Stats

    Args:
        df (DataFrame): Raw Advanced Stats DataFrame

    Returns:
        Pandas DataFrame of all Advanced Stats data 
    """
    try:
        df.drop(columns=df.columns[0], axis=1, inplace=True)
        df.columns = [
            "Team",
            "Age",
            "W",
            "L",
            "PW",
            "PL",
            "MOV",
            "SOS",
            "SRS",
            "ORTG",
            "DRTG",
            "NRTG",
            "Pace",
            "FTr",
            "3PAr",
            "TS%",
            "bby1",  # the bby columns are because of hierarchical html formatting - they're just blank columns
            "eFG%",
            "TOV%",
            "ORB%",
            "FT/FGA",
            "bby2",
            "eFG%_opp",
            "TOV%_opp",
            "DRB%_opp",
            "FT/FGA_opp",
            "bby3",
            "Arena",
            "Attendance",
            "Att/Game",
        ]
        df.drop(["bby1", "bby2", "bby3"], axis=1, inplace=True)
        df = df.query('Team != "League Average"').reset_index()
        # Playoff teams get a * next to them ??  fkn stupid, filter it out.
        df["Team"] = df["Team"].str.replace("*", "", regex=True)
        df["scrape_date"] = datetime.now().date()
        df.columns = df.columns.str.lower()
        logging.info(
            f"Advanced Stats Transformation Function Successful, retrieving updated data for 30 Teams"
        )
        return df
    except BaseException as error:
        logging.error(f"Advanced Stats Transformation Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df
