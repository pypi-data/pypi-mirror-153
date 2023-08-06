from datetime import datetime, timedelta
import os
from typing import List

from bs4 import BeautifulSoup
import logging
import numpy as np
import pandas as pd
import requests
import sentry_sdk

def schedule_scraper(year: str, month_list: List[str]) -> pd.DataFrame:
    """
    Web Scrape Function to scrape Schedule data by iterating through a list of months

    Args:
        year (str) - The year to scrape

        month_list (list) - List of full-month names to scrape
    
    Returns:
        DataFrame of Schedule Data to be stored.
    
    """
    try:
        schedule_df = pd.DataFrame()
        completed_months = []
        for i in month_list:
            url = f"https://www.basketball-reference.com/leagues/NBA_{year}_games-{i}.html"
            html = requests.get(url).content
            soup = BeautifulSoup(html, "html.parser")

            headers = [th.getText() for th in soup.findAll("tr")[0].findAll("th")]
            headers[6] = "boxScoreLink"
            headers[7] = "isOT"
            headers = headers[1:]

            rows = soup.findAll("tr")[1:]
            date_info = [
                [th.getText() for th in rows[i].findAll("th")] for i in range(len(rows))
            ]

            game_info = [
                [td.getText() for td in rows[i].findAll("td")] for i in range(len(rows))
            ]
            date_info = [i[0] for i in date_info]

            schedule = pd.DataFrame(game_info, columns=headers)
            schedule["Date"] = date_info

            logging.info(
                f"Schedule Function Completed for {i}, retrieving {len(schedule)} rows"
            )
            completed_months.append(i)
            schedule_df = schedule_df.append(schedule)

        schedule_df = schedule_df[
            ["Start (ET)", "Visitor/Neutral", "Home/Neutral", "Date"]
        ]
        schedule_df["proper_date"] = pd.to_datetime(schedule_df["Date"]).dt.date
        schedule_df.columns = schedule_df.columns.str.lower()
        schedule_df = schedule_df.rename(
            columns={
                "start (et)": "start_time",
                "visitor/neutral": "away_team",
                "home/neutral": "home_team",
            }
        )

        logging.info(
            f"Schedule Function Completed for {' '.join(completed_months)}, retrieving {len(schedule_df)} total rows"
        )
        return schedule_df
    except IndexError as index_error:
        logging.info(
            f"{i} currently has no data in basketball-reference, stopping the function and returning data for {' '.join(completed_months)}"
        )
        schedule_df = schedule_df[
            ["Start (ET)", "Visitor/Neutral", "Home/Neutral", "Date"]
        ]
        schedule_df["proper_date"] = pd.to_datetime(schedule_df["Date"]).dt.date
        schedule_df.columns = schedule_df.columns.str.lower()
        schedule_df = schedule_df.rename(
            columns={
                "start (et)": "start_time",
                "visitor/neutral": "away_team",
                "home/neutral": "home_team",
            }
        )
        return schedule_df
    except BaseException as e:
        logging.error(f"Schedule Scraper Function Failed, {e}")
        df = []
        return df