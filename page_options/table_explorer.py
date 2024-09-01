import streamlit as st
import pandas as pd

from commands.get_complete_table import get_complete_table
from commands.get_database_tables import get_database_tables

database = "finances_db"

tables = get_database_tables(database, clean=True)
selected_table = st.selectbox("Select a Table", tables)

if selected_table:
    df = pd.DataFrame(get_complete_table(database, selected_table))

    # Display the tabular view of the CSV file
    st.dataframe(df, use_container_width=True)

else:
    st.write("No table selected.")