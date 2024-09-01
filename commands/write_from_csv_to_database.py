import sqlite3
import pandas as pd

def write_from_csv_to_database(file_path, database, table_name):
    conn = sqlite3.connect(f"{database}.db")

    data = pd.read_csv(file_path, header=0, date_format="YYYY/MM/DD")

    date_fields = [
        'Posting Date',
        'Effective Date'
    ]

    for field in date_fields:
        if field in data.columns:
            data[field] = pd.to_datetime(data[field], format="%m/%d/%Y")

    data.to_sql(table_name, conn, if_exists='append', index=False)

    conn.commit()
    conn.close()