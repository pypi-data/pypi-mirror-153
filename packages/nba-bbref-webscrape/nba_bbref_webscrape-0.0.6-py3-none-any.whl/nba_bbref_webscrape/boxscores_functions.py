import os
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import logging
import pandas as pd
import requests
import sentry_sdk

today = datetime.now().date()
todaytime = datetime.now()
yesterday = today - timedelta(1)
day = (datetime.now() - timedelta(1)).day
month = (datetime.now() - timedelta(1)).month
year = (datetime.now() - timedelta(1)).year

if today < datetime(2022, 4, 11).date():
    season_type = "Regular Season"
elif (today >= datetime(2022, 4, 11).date()) & (today < datetime(2022, 4, 16).date()):
    season_type = "Play-In"
else:
    season_type = "Playoffs"


def get_boxscores_data(month=month, day=day, year=year):
    """
    Function that grabs box scores from a given date in mmddyyyy format - defaults to yesterday.  values can be ex. 1 or 01.
    Can't use read_html for this so this is raw web scraping baby.

    Args:
        month (string): month value of the game played (0 - 12)

        day (string): day value of the game played (1 - 31)

        year (string): year value of the game played (2021)

    Returns:
        DataFrame of Player Aggregate Season stats
    """
    url = f"https://www.basketball-reference.com/friv/dailyleaders.fcgi?month={month}&day={day}&year={year}&type=all"

    try:
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        headers = [th.getText() for th in soup.findAll("tr", limit=2)[0].findAll("th")]
        headers = headers[1:]
        headers[1] = "Team"
        headers[2] = "Location"
        headers[3] = "Opponent"
        headers[4] = "Outcome"
        headers[6] = "FGM"
        headers[8] = "FGPercent"
        headers[9] = "threePFGMade"
        headers[10] = "threePAttempted"
        headers[11] = "threePointPercent"
        headers[14] = "FTPercent"
        headers[15] = "OREB"
        headers[16] = "DREB"
        headers[24] = "PlusMinus"

        rows = soup.findAll("tr")[1:]
        player_stats = [
            [td.getText() for td in rows[i].findAll("td")] for i in range(len(rows))
        ]

        df = pd.DataFrame(player_stats, columns=headers)
        return df
    except IndexError as error:
        logging.warning(
            f"Box Score Extraction Function Failed, {error}, no data available for {year}-{month}-{day}"
        )
        sentry_sdk.capture_exception(error)
        df = []
        return df
    except BaseException as error:
        logging.error(f"Box Score Extraction Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df


def get_boxscores_transformed(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformation Function for boxscores that gets stored to SQL and is used as an input for PBP Function.
    Player names get accents removed & team acronyms get normalized here.

    Args:
        df (DataFrame): Raw Boxscores DataFrame

    Returns:
        DataFrame of transformed boxscores.
    """
    try:
        df[
            [
                "FGM",
                "FGA",
                "FGPercent",
                "threePFGMade",
                "threePAttempted",
                "threePointPercent",
                "OREB",
                "DREB",
                "TRB",
                "AST",
                "STL",
                "BLK",
                "TOV",
                "PF",
                "PTS",
                "PlusMinus",
                "GmSc",
            ]
        ] = df[
            [
                "FGM",
                "FGA",
                "FGPercent",
                "threePFGMade",
                "threePAttempted",
                "threePointPercent",
                "OREB",
                "DREB",
                "TRB",
                "AST",
                "STL",
                "BLK",
                "TOV",
                "PF",
                "PTS",
                "PlusMinus",
                "GmSc",
            ]
        ].apply(
            pd.to_numeric
        )
        df["date"] = str(year) + "-" + str(month) + "-" + str(day)
        df["date"] = pd.to_datetime(df["date"])
        df["Type"] = season_type
        df["Season"] = 2022
        df["Location"] = df["Location"].apply(lambda x: "A" if x == "@" else "H")
        df["Team"] = df["Team"].str.replace("PHO", "PHX")
        df["Team"] = df["Team"].str.replace("CHO", "CHA")
        df["Team"] = df["Team"].str.replace("BRK", "BKN")
        df["Opponent"] = df["Opponent"].str.replace("PHO", "PHX")
        df["Opponent"] = df["Opponent"].str.replace("CHO", "CHA")
        df["Opponent"] = df["Opponent"].str.replace("BRK", "BKN")
        df = df.query("Player == Player").reset_index(drop=True)
        df["Player"] = (
            df["Player"]
            .str.normalize("NFKD")  # this is removing all accented characters
            .str.encode("ascii", errors="ignore")
            .str.decode("utf-8")
        )
        df.columns = df.columns.str.lower()
        logging.info(
            f"Box Score Transformation Function Successful, retrieving {len(df)} rows for {year}-{month}-{day}"
        )
        return df
    except TypeError as error:
        logging.warning(
            f"Box Score Transformation Function Failed, {error}, no data available for {year}-{month}-{day}"
        )
        sentry_sdk.capture_exception(error)
        df = []
        return df
    except BaseException as error:
        logging.error(f"Box Score Transformation Function Logic Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df