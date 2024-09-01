import pandas as pd

def get_dataframe_from_query(query, database):
    data = pd.read_sql_query(query, f"sqlite:///{database}.db")
    return data