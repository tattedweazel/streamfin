import pandas as pd

def get_complete_table(database, table_name):
    return pd.read_sql_table(table_name, f"sqlite:///{database}.db")