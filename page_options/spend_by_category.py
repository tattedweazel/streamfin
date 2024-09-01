import streamlit as st
import plotly.express as px
import pandas as pd

from commands.get_database_tables import get_database_tables

database = 'finances_db'

if "cleaned_records" not in get_database_tables(database, clean=True):
    st.warning("No cleaned records found. Reporting unavailable.")

# Filter by dates
start_date = st.date_input("Start Date", format="YYYY/MM/DD", value=pd.to_datetime("2023/01/01"))
end_date = st.date_input("End Date", format="YYYY/MM/DD")

# Fetch the cleaned records from the database
query = f"""
            SELECT
                ec.category_name AS Category,
                sum(ce.Amount) * -1 AS Total
            FROM cleaned_records ce 
            INNER JOIN entity_category ec ON ce.Entity = ec.entity_name
            WHERE (ce.Date >= '{start_date}' AND ce.Date < '{end_date}')
            GROUP BY 1
            ORDER BY 2 desc

            """
cleaned_records = pd.read_sql_query(query, f"sqlite:///{database}.db")

st.dataframe(cleaned_records, use_container_width=True)


fig = px.bar(cleaned_records.set_index('Category')['Total'], title='Total Spend by Category')
st.plotly_chart(fig)


# st.dataframe(cleaned_records.set_index('Category'), use_container_width=True)