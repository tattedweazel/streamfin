import streamlit as st
import sqlite3


def drop_table(database, table_name):
    # Connect to the database
    conn = sqlite3.connect(f'{database}.db')
    cursor = conn.cursor()

    # Construct the SQL query
    query = f"DROP TABLE {table_name}"

    st.write(f"Dropping table: {table_name}")
    st.write("Query:", query)

    # Execute the query
    cursor.execute(query)
    conn.commit()

    # Close the connection
    conn.close()