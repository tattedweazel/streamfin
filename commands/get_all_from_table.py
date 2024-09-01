import sqlite3

def get_all_from_table(database_name, table_name, columns_str="*"):
    # Connect to the SQLite database
    conn = sqlite3.connect(f"{database_name}.db")

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    query = f"SELECT {columns_str} FROM {table_name};"
    cursor.execute(query)
    tables = cursor.fetchall()

    conn.close()

    return tables