import os
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
import logging
import numpy as np
import pandas as pd
import requests
import sentry_sdk

def get_transactions_data():
    """
    Web Scrape function w/ BS4 that retrieves NBA Trades, signings, waivers etc.

    Args:
        None

    Returns:
        Pandas DataFrame of all season transactions, trades, player waives etc.
    """
    try:
        url = "https://www.basketball-reference.com/leagues/NBA_2022_transactions.html"
        html = requests.get(url).content
        soup = BeautifulSoup(html, "html.parser")
        # theres a bunch of garbage in the first 50 rows - no matter what
        trs = soup.findAll("li")[70:]
        rows = []
        mylist = []
        for tr in trs:
            date = tr.find("span")
            # needed bc span can be null (multi <p> elements per span)
            if date is not None:
                date = date.text
            data = tr.findAll("p")
            for p in data:
                mylist.append(p.text)
            data3 = [date] + [mylist]
            rows.append(data3)
            mylist = []

        transactions = pd.DataFrame(rows)
        logging.info(
            f"Transactions Web Scrape Function Successful, retrieving {len(transactions)} rows"
        )
        return transactions
    except BaseException as error:
        logging.error(f"Transaction Web Scrape Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df


def get_transactions_transformed(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformation function for Transactions data

    Args:
        df (DataFrame): Raw Transactions DataFrame

    Returns:
        Pandas DataFrame of all Transactions data 
    """
    transactions = df
    try:
        transactions.columns = ["Date", "Transaction"]
        transactions = transactions.query(
            'Date == Date & Date != ""'
        ).reset_index()  # filters out nulls and empty values
        transactions = transactions.explode("Transaction")
        transactions["Date"] = transactions["Date"].str.replace(
            "?", "Jan 1, 2021", regex=True  # bad data 10-14-21
        )
        transactions["Date"] = pd.to_datetime(transactions["Date"])
        transactions.columns = transactions.columns.str.lower()
        transactions = transactions[["date", "transaction"]]
        transactions["scrape_date"] = datetime.now().date()
        logging.info(
            f"Transactions Transformation Function Successful, retrieving {len(transactions)} rows"
        )
        return transactions
    except BaseException as error:
        logging.error(f"Transaction Transformation Function Failed, {error}")
        sentry_sdk.capture_exception(error)
        df = []
        return df
