import sqlite3

def remove_from_table(database, table, column_name, value, where_str=None):
    # Connect to the database
    conn = sqlite3.connect(f'{database}.db')
    cursor = conn.cursor()

    # Construct the SQL query
    if where_str is not None:
        query = f"DELETE FROM {table} WHERE {where_str};"
        cursor.execute(query)
    else:
        query = f"DELETE FROM {table} WHERE {column_name} = ?"
        cursor.execute(query, (value,))

    # Execute the query
    
    conn.commit()
    print(query)
    # Close the connection
    conn.close()