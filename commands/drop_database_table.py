import sqlite3

def drop_database_table(database_name, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(f"{database_name}.db")
    c = conn.cursor()

    # Drop the table
    c.execute(f"DROP TABLE IF EXISTS {table_name}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    return True