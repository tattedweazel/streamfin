import os
import pandas as pd
import streamlit as st

from commands.append_to_table import append_to_table
from commands.get_database_tables import get_database_tables
from commands.get_list_of_values_from_column import get_list_of_values_from_column
from commands.remove_from_table import remove_from_table

database = "finances_db"
patterns_table = "transform_pattern"

st.subheader("Transform Pattern Table")
# Query the SQLite database for all records in the "transform_pattern" table
if patterns_table in get_database_tables(database, clean=True):
    transform_pattern_df = pd.read_sql_table(patterns_table, f"sqlite:///{database}.db")
    st.write(transform_pattern_df)

# Add new records to the "transform_pattern" table
with st.expander("Add New Record"):
    pattern = st.text_input("Pattern")
    clean_description = st.text_input("Clean Description")
    if st.button("Add Record", key="add_record"):
        new_record = pd.DataFrame([{"pattern": pattern, "clean_description": clean_description}])
        append_to_table(database, patterns_table, new_record)
        st.success(f"Record added to '{patterns_table}' table.")
        st.rerun()

with st.expander("Remove a Pattern"):
    if patterns_table in get_database_tables(database, clean=True):
        selected_record = st.selectbox("Select a pattern to remove", get_list_of_values_from_column(database, patterns_table, "pattern"))
        remove_record_button = st.button("Remove Record", key="remove_record")
        if remove_record_button:
            transform_pattern_df = transform_pattern_df[transform_pattern_df["pattern"] != selected_record]
            remove_from_table(database, patterns_table, "pattern", selected_record)
            st.success(f"Record removed from '{patterns_table}' table.")
            st.rerun()

with st.expander("Import Records"):
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    if uploaded_file is not None:
        # Check if the uploaded file is a CSV file
        if uploaded_file.type == 'text/csv':
            # Store the uploaded file to a local directory
            file_path = os.path.join('uploads', uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            st.success("File uploaded successfully!")
        else:
            st.error("Please upload a CSV file.")

with st.expander("Export Records"):
    if st.button("Export CSV"):
        transform_pattern_df.to_csv("exports/transform_pattern.csv", index=False)
        st.success("CSV file exported successfully.")