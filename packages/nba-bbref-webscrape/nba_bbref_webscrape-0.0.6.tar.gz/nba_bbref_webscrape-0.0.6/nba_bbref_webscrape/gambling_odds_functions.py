import os
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import logging
import numpy as np
import pandas as pd
import requests
import sentry_sdk

year = (datetime.now() - timedelta(1)).year

def get_odds_data():
    """
    Web Scrape function w/ pandas read_html that grabs current day's nba odds in raw format.
    There are 2 objects [0], [1] if the days are split into 2.
    AWS ECS operates in UTC time so the game start times are actually 5-6+ hours ahead of what they actually are, so there are 2 html tables.

    Args:
        None
    Returns:
        Pandas DataFrame of NBA moneyline + spread odds for upcoming games for that day
    """
    try:
        url = "https://sportsbook.draftkings.com/leagues/basketball/88670846?category=game-lines&subcategory=game"
        df = pd.read_html(url)
        logging.info(
            f"Odds Web Scrape Function Successful {len(df)} day, retrieving {len(df)} day objects"
        )
        return df
    except (
        BaseException,
        ValueError,
    ) as error:  # valueerror fucked shit up apparently idfk
        logging.error(f"Odds Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df


# import pickle
# with open('tests/fixture_csvs/odds_data', 'wb') as fp:
#     pickle.dump(df, fp)


def get_odds_transformed(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformation function for Odds Data

    Args:
        df (DataFrame): Raw Odds DataFrame

    Returns:
        Pandas DataFrame of all Odds Data 
    """
    if len(df) == 0:
        logging.info(f"Odds Transformation Failed, no Odds Data available.")
        df = []
        return df
    else:
        try:
            data1 = df[0].copy()
            data1.columns.values[0] = "Tomorrow"
            date_try = str(year) + " " + data1.columns[0]
            data1["date"] = np.where(
                date_try == "2022 Tomorrow",
                datetime.now().date(),  # if the above is true, then return this
                str(year) + " " + data1.columns[0],  # if false then return this
            )
            # )
            date_try = data1["date"].iloc[0]
            data1.reset_index(drop=True)
            data1["Tomorrow"] = data1["Tomorrow"].str.replace(
                "LA Clippers", "LAC Clippers", regex=True
            )

            data1["Tomorrow"] = data1["Tomorrow"].str.replace("AM", "AM ", regex=True)
            data1["Tomorrow"] = data1["Tomorrow"].str.replace("PM", "PM ", regex=True)
            data1["Time"] = data1["Tomorrow"].str.split().str[0]
            data1["datetime1"] = (
                pd.to_datetime(date_try.strftime("%Y-%m-%d") + " " + data1["Time"])
                - timedelta(hours=6)
                + timedelta(days=1)
            )
            if len(df) > 1:  # if more than 1 day's data appears then do this
                data2 = df[1].copy()
                data2.columns.values[0] = "Tomorrow"
                data2.reset_index(drop=True)
                data2["Tomorrow"] = data2["Tomorrow"].str.replace(
                    "LA Clippers", "LAC Clippers", regex=True
                )
                data2["Tomorrow"] = data2["Tomorrow"].str.replace(
                    "AM", "AM ", regex=True
                )
                data2["Tomorrow"] = data2["Tomorrow"].str.replace(
                    "PM", "PM ", regex=True
                )
                data2["Time"] = data2["Tomorrow"].str.split().str[0]
                data2["datetime1"] = (
                    pd.to_datetime(date_try.strftime("%Y-%m-%d") + " " + data2["Time"])
                    - timedelta(hours=6)
                    + timedelta(days=1)
                )
                data2["date"] = data2["datetime1"].dt.date

                data = data1.append(data2).reset_index(drop=True)
                data["SPREAD"] = data["SPREAD"].str[:-4]
                data["TOTAL"] = data["TOTAL"].str[:-4]
                data["TOTAL"] = data["TOTAL"].str[2:]
                data["Tomorrow"] = data["Tomorrow"].str.split().str[1:2]
                data["Tomorrow"] = pd.DataFrame(
                    [
                        str(line).strip("[").strip("]").replace("'", "")
                        for line in data["Tomorrow"]
                    ]
                )
                data["SPREAD"] = data["SPREAD"].str.replace("pk", "-1", regex=True)
                data["SPREAD"] = data["SPREAD"].str.replace("+", "", regex=True)
                data.columns = data.columns.str.lower()
                data = data[
                    ["tomorrow", "spread", "total", "moneyline", "date", "datetime1"]
                ]
                data = data.rename(columns={data.columns[0]: "team"})
                data = data.query(
                    "date == date.min()"
                )  # only grab games from upcoming day
                logging.info(
                    f"Odds Transformation Function Successful {len(df)} day, retrieving {len(data)} rows"
                )
                return data
            else:  # if there's only 1 day of data then just use that
                data = data1.reset_index(drop=True)
                data["SPREAD"] = data["SPREAD"].str[:-4]
                data["TOTAL"] = data["TOTAL"].str[:-4]
                data["TOTAL"] = data["TOTAL"].str[2:]
                data["Tomorrow"] = data["Tomorrow"].str.split().str[1:2]
                data["Tomorrow"] = pd.DataFrame(
                    [
                        str(line).strip("[").strip("]").replace("'", "")
                        for line in data["Tomorrow"]
                    ]
                )
                data["SPREAD"] = data["SPREAD"].str.replace("pk", "-1", regex=True)
                data["SPREAD"] = data["SPREAD"].str.replace("+", "", regex=True)
                data.columns = data.columns.str.lower()
                data = data[
                    ["tomorrow", "spread", "total", "moneyline", "date", "datetime1"]
                ]
                data = data.rename(columns={data.columns[0]: "team"})
                data = data.query(
                    "date == date.min()"
                )  # only grab games from upcoming day
                logging.info(
                    f"Odds Transformation Function Successful {len(df)} day, retrieving {len(data)} rows"
                )
                return data
        except BaseException as error:
            logging.error(
                f"Odds Transformation Function Failed for {len(df)} day objects, {error}"
            )
            sentry_sdk.capture_exception(error)
            data = []
            return data
