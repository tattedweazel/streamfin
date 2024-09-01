import streamlit as st

from commands.get_database_tables import get_database_tables
from commands.drop_database_table import drop_database_table
import sqlite3

# --- Functions
def perform_delete(database, table):
    if drop_database_table('finances_db', table_name):
        st.write(f"{table_name} dropped successfully!")
    else:
        st.write(f"Failed to drop {table_name}.")


# Display the list of tables in the Streamlit app
st.write("Currently available Tables:")
for table in get_database_tables('finances_db'):
    table_name = table[0]

    col1, col2 = st.columns(2)
    with col1:
        st.write(table_name)
    with col2:
        with st.expander("Delete"):
            delete_button = st.button(f"Delete {table_name}")

    if delete_button:
        perform_delete('finances_db', table_name)
        st.rerun()