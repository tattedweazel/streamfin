import sqlite3

def get_database_tables(database_name, clean=False):
    # Connect to the SQLite database
    conn = sqlite3.connect(f"{database_name}.db")

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Get the list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if clean:
        tables = [table[0] for table in tables]

    # Close the database connection
    conn.close()

    return tables