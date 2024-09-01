import sqlite3
import pandas as pd


def get_list_of_values_from_column(database, table_name, column_name):
    """ Query the SQLite database for all unique values in a column of a table """
    conn = sqlite3.connect(f"{database}.db")
    query = f"SELECT DISTINCT {column_name} FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df[column_name].unique()
