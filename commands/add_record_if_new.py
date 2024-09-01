import sqlite3
import pandas as pd


def add_record_if_new(database, table, dataframe):
    """ Add or update a record in a SQLite database table """
    # Connect to the database
    conn = sqlite3.connect(f'{database}.db')

    dataframe.to_sql(table, conn, if_exists='append', index=False)
    conn.commit() 
    conn.close()

    