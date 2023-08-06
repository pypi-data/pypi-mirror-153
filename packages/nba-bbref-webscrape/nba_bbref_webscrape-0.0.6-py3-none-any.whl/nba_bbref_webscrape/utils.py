import pandas as pd
import logging
import sentry_sdk

def get_leading_zeroes(month: int) -> str:
    """
    Function to add leading zeroes to a month (1 (January) -> 01) for the write_to_s3 function.

    Args:
        month (int): The month integer
    
    Returns:
        The same month integer with a leading 0 if it is less than 10 (Nov/Dec aka 11/12 unaffected).
    """
    if len(str(month)) > 1:
        return month
    else:
        return f"0{month}"

def clean_player_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to remove suffixes from player names for joining downstream.
    Assumes the column name is ['player']

    Args:
        df (DataFrame): The DataFrame you wish to alter
    
    Returns:
        df with transformed player names
    """
    try:
        df["player"] = df["player"].str.replace(" Jr.", "", regex=True)
        df["player"] = df["player"].str.replace(" Sr.", "", regex=True)
        df["player"] = df["player"].str.replace(
            " III", "", regex=True
        )  # III HAS TO GO FIRST, OVER II
        df["player"] = df["player"].str.replace(
            " II", "", regex=True
        )  # Robert Williams III -> Robert WilliamsI
        df["player"] = df["player"].str.replace(" IV", "", regex=True)
        return df
    except BaseException as e:
        logging.error(f"Error Occurred with clean_player_names, {e}")
        sentry_sdk.capture_exception(e)
