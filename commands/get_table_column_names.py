import sqlite3

def get_table_column_names(database, table_name, as_str=False):
    conn = sqlite3.connect(f'{database}.db')  # Replace 'your_database.db' with your actual database file name
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    conn.close()

    if as_str:
        return ', '.join([column[1] for column in columns])
    else:
        return [column[1] for column in columns]