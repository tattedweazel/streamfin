import streamlit as st


import os

from commands.get_database_tables import get_database_tables
from commands.write_from_csv_to_database import write_from_csv_to_database

database = "finances_db"


# Function to load CSV data into the database
def write_data(file_path, table_name):
    if file_path and table_name:
        write_from_csv_to_database(file_path, database, table_name)
        st.success(f"Data written to {table_name}.")

st.title("CSV to SQLite Database Loader")

file_names = os.listdir("uploads")
file_path = st.selectbox("Select CSV file", file_names)
file_path = os.path.join("uploads", file_path) if file_path else None

with st.expander("To Existing Table"):
    selected_table = st.selectbox("Select a file to delete", get_database_tables(database, clean=True))
    write_to_table_button = st.button("Write to Table", key="write_to_table")
    if write_to_table_button:
        table_name = selected_table
        write_data(file_path, table_name)

with st.expander("To New Table"):
    table_name = st.text_input("Table Name")
    make_new_button = st.button("Make new table", key="make_new_table")
    if make_new_button:
        write_data(file_path, table_name)


