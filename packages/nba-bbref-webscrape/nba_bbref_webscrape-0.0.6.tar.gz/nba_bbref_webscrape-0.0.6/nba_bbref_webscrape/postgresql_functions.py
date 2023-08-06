from datetime import datetime, timedelta
import logging
import os
from typing import List
import uuid

import pandas as pd
import sentry_sdk
from sqlalchemy import exc, create_engine

def write_to_sql(con, table_name: str, df: pd.DataFrame, table_type: str):
    """
    SQL Table function to write a pandas data frame in aws_dfname_source format

    Args:
        con (SQL Connection): The connection to the SQL DB.

        table_name (str): The Table name to write to SQL as.

        df (DataFrame): The Pandas DataFrame to store in SQL

        table_type (str): Whether the table should replace or append to an existing SQL Table under that name

    Returns:
        Writes the Pandas DataFrame to a Table in Snowflake in the {nba_source} Schema we connected to.

    """
    try:
        if len(df) == 0:
            logging.info(f"{table_name} is empty, not writing to SQL")
        elif df.schema == "Validated":
            df.to_sql(
                con=con,
                name=f"aws_{table_name}_source",
                index=False,
                if_exists=table_type,
            )
            logging.info(
                f"Writing {len(df)} {table_name} rows to aws_{table_name}_source to SQL"
            )
        else:
            logging.info(f"{table_name} Schema Invalidated, not writing to SQL")
    except BaseException as error:
        logging.error(f"SQL Write Script Failed, {error}")
        sentry_sdk.capture_exception(error)
        return error


def write_to_sql_upsert(
    conn, table_name: str, df: pd.DataFrame, table_type: str, pd_index: List[str]
):
    """
    SQL Table function to upsert a Pandas DataFrame into a SQL Table.

    Will create a new table if it doesn't exist.  If it does, it will insert new records and upsert new column values onto existing records (if applicable).

    You have to do some extra index stuff to the pandas df to specify what the primary key of the records is (this data does not get upserted).

    Args:
        conn (SQL Connection): The connection to the SQL DB.

        table_name (str): The Table name to write to SQL as.

        df (DataFrame): The Pandas DataFrame to store in SQL

        table_type (str): A placeholder which should always be "upsert"

    Returns:
        Upserts any new data in the Pandas DataFrame to the table in Postgres in the {nba_source_dev} schema

    """
    try:
        df = df.set_index(pd_index)
        df = df.rename_axis(pd_index)
        sql_table_name = f"aws_{table_name}_source"

        # If the table does not exist, we should just use to_sql to create it - schema is hardcoded in
        if not conn.execute(
            f"""SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE  table_schema = 'nba_source' 
                AND    table_name   = '{sql_table_name}');
                """
        ).first()[0]:
            df.to_sql(sql_table_name, conn)
            print(
                f"SQL Upsert Function Successful, {len(df)} records added to a NEW table {sql_table_name}"
            )
            pass
        else:
            # If it already exists...
            temp_table_name = f"temp_{uuid.uuid4().hex[:6]}"
            df.to_sql(temp_table_name, conn, index=True)
            # use to_sql to create a "temp" table, then drop it at the end.

            index = list(df.index.names)
            index_sql_txt = ", ".join([f'"{i}"' for i in index])
            columns = list(df.columns)
            headers = index + columns
            headers_sql_txt = ", ".join([f'"{i}"' for i in headers])
            # this is excluding the primary key columns needed to identify the unique rows.
            update_column_stmt = ", ".join(
                [f'"{col}" = EXCLUDED."{col}"' for col in columns]
            )

            # For the ON CONFLICT clause, postgres requires that the columns have unique constraint
            query_pk = f"""
            ALTER TABLE "{sql_table_name}" DROP CONSTRAINT IF EXISTS unique_constraint_for_upsert;
            ALTER TABLE "{sql_table_name}" ADD CONSTRAINT unique_constraint_for_upsert UNIQUE ({index_sql_txt});
            """

            conn.execute(query_pk)

            # Compose and execute upsert query
            query_upsert = f"""
            INSERT INTO "{sql_table_name}" ({headers_sql_txt}) 
            SELECT {headers_sql_txt} FROM "{temp_table_name}"
            ON CONFLICT ({index_sql_txt}) DO UPDATE 
            SET {update_column_stmt};
            """
            conn.execute(query_upsert)
            conn.execute(f"DROP TABLE {temp_table_name};")
            print(
                f"SQL Upsert Function Successful, {len(df)} records added or upserted into {table_name}"
            )
            pass
    except BaseException as error:
        conn.execute(f"DROP TABLE {temp_table_name};")
        print(f"SQL Upsert Function Failed for {table_name} ({len(df)} rows), {error}")
        pass


def sql_connection(rds_schema: str):
    """
    SQL Connection function connecting to my postgres db with schema = nba_source where initial data in ELT lands.

    Args:
        rds_schema (str): The Schema in the DB to connect to.

    Returns:
        SQL Connection variable to a specified schema in my PostgreSQL DB
    """
    RDS_USER = os.environ.get("RDS_USER")
    RDS_PW = os.environ.get("RDS_PW")
    RDS_IP = os.environ.get("IP")
    RDS_DB = os.environ.get("RDS_DB")
    try:
        connection = create_engine(
            f"postgresql+psycopg2://{RDS_USER}:{RDS_PW}@{RDS_IP}:5432/{RDS_DB}",
            connect_args={"options": f"-csearch_path={rds_schema}"},
            # defining schema to connect to
            echo=False,
        )
        logging.info(f"SQL Connection to schema: {rds_schema} Successful")
        return connection
    except exc.SQLAlchemyError as e:
        logging.error(f"SQL Connection to schema: {rds_schema} Failed, Error: {e}")
        sentry_sdk.capture_exception(e)
        return e