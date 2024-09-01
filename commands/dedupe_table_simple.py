import sqlite3
import pandas as pd

def dedupe_table_simple(database_name, table_name, columns):
    # Connect to the database
    conn = sqlite3.connect(f"{database_name}.db")
    cursor = conn.cursor()

    # Create a temporary table to store distinct rows
    temp_table_name = f"{table_name}_temp"
    cursor.execute(f"CREATE TABLE {temp_table_name} AS SELECT DISTINCT {columns} FROM {table_name}")

    # Drop the original table
    cursor.execute(f"DROP TABLE {table_name}")

    # Rename the temporary table to the original table name
    cursor.execute(f"ALTER TABLE {temp_table_name} RENAME TO {table_name}")

    conn.commit()
    conn.close()
