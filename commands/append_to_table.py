import sqlite3
import pandas as pd

def append_to_table(database, table_name, dataframe):
    conn = sqlite3.connect(f"{database}.db")
    dataframe.to_sql(table_name, conn, if_exists='append', index=False)
    conn.commit()
    conn.close()