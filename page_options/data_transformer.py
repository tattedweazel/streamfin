import streamlit as st

from commands.dedupe_table_simple import dedupe_table_simple
from commands.get_database_tables import get_database_tables
from commands.get_database_tables_by_prefix import get_database_tables_by_prefix
from commands.add_record_if_new import add_record_if_new

import pandas as pd

database = "finances_db"
patterns_table = "transform_pattern"

st.title("Let's get transforming!")

# Use streamlit to create a selector for the tables
selected_table = st.selectbox("Select a table", get_database_tables_by_prefix(database, 'tx_', clean=True), key="selected_table")

if selected_table:
    # Read the selected table into a pandas DataFrame
    df = pd.read_sql_table(selected_table, f"sqlite:///{database}.db")

    # Query the SQLite database for all records in the "transform_pattern" table
    if patterns_table in get_database_tables(database, clean=True):
        transform_pattern_df = pd.read_sql_table(patterns_table, f"sqlite:///{database}.db")

    hits = []
    misses = []

    if "Amount" in df.columns:
        for index, row in df.iterrows():
            record = {
                "Amount": row["Amount"],
                "Date": row["Posting Date"],
                "TransactionId": row["Transaction ID"].replace(' ', '').replace(',',''),
            }

            # Check if "Description" is matched by any patterns in the transform_pattern_df
            matched = False
            for _, pattern_row in transform_pattern_df.iterrows():
                pattern = pattern_row["pattern"]
                if pattern in row["Description"]:
                    record["Entity"] = pattern_row["clean_description"]
                    hits.append(record)
                    matched = True
                    break

            # If no match is found, add "Description" property to the record and add it to the "misses" list
            if not matched:
                record["Description"] = row["Description"]
                misses.append(record)

    # Display hits and misses in separate tables
    st.subheader("Hits")
    hits_df = pd.DataFrame(hits)
    st.dataframe(hits_df, use_container_width=True, hide_index=True)

    st.subheader("Misses")
    misses_df = pd.DataFrame(misses)
    st.dataframe(misses_df, use_container_width=True)

    if not misses and hits:
        st.success("All records matched, and we're good for import!")
        release_button = st.button("Upsert cleaned records to Database", key="release_button")
        if release_button:
            st.write(hits_df)
            add_record_if_new(database, "cleaned_records", hits_df)
            dedupe_table_simple(database, "cleaned_records", "Amount, Date, TransactionId, Entity")
            
            st.success(f"Migration Complete!")

    elif misses:
        st.subheader("Add Entities")

        for index, row in misses_df.iterrows():
            description = row["Description"]
            record = {
                "Description": description,
                "Entity": None
            }

            with st.expander(f"Description: {description}"):
                col1, col2, col3 = st.columns(3, vertical_alignment="bottom", gap="medium")
                with col1:
                    pattern_input = st.text_input("Pattern", key=f"pattern_{index}", value=description, on_change=None)
                with col2:
                    entity_input = st.text_input("Entity", key=f"entity_{index}", on_change=None)
                with col3:
                    create_button = st.button("Create Pattern", key=f"create_pattern_{index}")
                    if create_button:
                        add_record_if_new(database, patterns_table, pd.DataFrame([{"pattern": pattern_input, "clean_description": entity_input}]))
                        st.success(f"Pattern added to the transform_pattern table")
                        st.rerun()