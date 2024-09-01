import streamlit as st
import pandas as pd

from commands.get_database_tables import get_database_tables

database = 'finances_db'

if "cleaned_records" not in get_database_tables(database, clean=True):
    st.warning("No cleaned records found. Reporting unavailable.")

# Filter by dates
start_date = st.date_input("Start Date", format="YYYY/MM/DD", value=pd.to_datetime("2023/01/01"))
end_date = st.date_input("End Date", format="YYYY/MM/DD")

# Fetch the cleaned records from the database
query = f"SELECT Entity, SUM(Amount) * -1 AS Total FROM cleaned_records WHERE Amount < 0 AND (Date >= '{start_date}' AND Date < '{end_date}') GROUP BY Entity ORDER BY 2 desc"
cleaned_records = pd.read_sql_query(query, f"sqlite:///{database}.db")


st.dataframe(cleaned_records.set_index('Entity')['Total'], use_container_width=True)
