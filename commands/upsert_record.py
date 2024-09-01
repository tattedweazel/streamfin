import sqlite3

def upsert_record(database, table, record, key, update=True):
    """ Add or update a record in a SQLite database table """
    # Connect to the database
    conn = sqlite3.connect(f'{database}.db')
    cursor = conn.cursor()

    # Construct the SQL query
    query = f"SELECT * FROM {table} WHERE {key} = ?"
    cursor.execute(query, (record[key],))
    result = cursor.fetchone()

    if result and update:
        # Update the record
        query = f"UPDATE {table} SET "
        query += ", ".join([f"{column} = ?" for column in record.keys()])
        query += f" WHERE {key} = ?"
        cursor.execute(query, list(record.values()) + [record[key]])
    else:
        # Add the record
        query = f"INSERT INTO {table} ({', '.join(record.keys())}) VALUES ({', '.join(['?'] * len(record))})"
        cursor.execute(query, list(record.values()))

    conn.commit()
    conn.close()