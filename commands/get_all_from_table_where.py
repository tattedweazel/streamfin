import sqlite3

def get_all_from_table_where(database_name, table_name, where_str = True, columns_str="*"):
    # Connect to the SQLite database
    conn = sqlite3.connect(f"{database_name}.db")

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    query = f"SELECT {columns_str} FROM {table_name} WHERE {where_str};"
    cursor.execute(query)
    results = cursor.fetchall()

    conn.close()

    return results