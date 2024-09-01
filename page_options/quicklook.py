import streamlit as st
import plotly.express as px
import pandas as pd

from commands.get_dataframe_from_query import get_dataframe_from_query
from datetime import datetime, timedelta


database = 'finances_db'


# --- Functions

def get_transactions_by_category_between_dates(start_date, end_date):
    # Query to join the cleaned_record and category tables
    query = f"""
        SELECT 
            ec.category_name AS CategoryName, 
            COUNT(DISTINCT cr.TransactionID) AS NumberOfTransactions, 
            SUM(cr.Amount * -1.0) AS TotalSpent
        FROM cleaned_records AS cr
        JOIN entity_category AS ec ON cr.Entity = ec.entity_name
        WHERE (cr.Date >= '{start_date}' AND cr.Date < '{end_date}')
        AND cr.Amount < 0
        GROUP BY ec.category_name
        ORDER BY TotalSpent DESC"""

    # Execute the query and fetch the results into a pandas DataFrame
    return get_dataframe_from_query(query, database)

def get_transactions_by_entity_between_dates(start_date, end_date):
    # Query to join the cleaned_record and category tables
    query = f"""
        SELECT 
            cr.Entity AS EntityName, 
            COUNT(DISTINCT cr.TransactionID) AS NumberOfTransactions, 
            SUM(cr.Amount * -1.0) AS TotalSpent
        FROM cleaned_records AS cr
        WHERE (cr.Date >= '{start_date}' AND cr.Date < '{end_date}')
        AND cr.Amount < 0
        GROUP BY 1
        ORDER BY 3 DESC"""

    # Execute the query and fetch the results into a pandas DataFrame
    return get_dataframe_from_query(query, database)

def rate_of_change(current, previous):
    return (current - previous) / previous * 100


st.subheader("Last X Days")
date_option = st.selectbox("Date Range", [30,60,90,180,365])

# Calculate the start and end dates based on the selected option
if date_option == 30:
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    prev_end_date = start_date - timedelta(days=1)
    prev_start_date = prev_end_date - timedelta(days=30)
elif date_option == 60:
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=60)
    prev_end_date = start_date - timedelta(days=1)
    prev_start_date = prev_end_date - timedelta(days=60)
elif date_option == 90:
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=90)
    prev_end_date = start_date - timedelta(days=1)
    prev_start_date = prev_end_date - timedelta(days=90)
elif date_option == 180:
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=180)
    prev_end_date = start_date - timedelta(days=1)
    prev_start_date = prev_end_date - timedelta(days=180)
elif date_option == 365:
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=365)
    prev_end_date = start_date - timedelta(days=1)
    prev_start_date = prev_end_date - timedelta(days=365)
        

# Get the transactions between the start date and end date
category_transactions_df = get_transactions_by_category_between_dates(start_date, end_date)

total_spent = category_transactions_df['TotalSpent'].sum()

# Calculate the total income
income_query = f"""
    SELECT 
        SUM(cr.Amount) AS TotalIncome
    FROM cleaned_records AS cr
    WHERE (cr.Date >= '{start_date}' AND cr.Date < '{end_date}')
    AND cr.Amount > 0
"""

income_result = get_dataframe_from_query(income_query, database)
total_income = income_result['TotalIncome'].values[0]

# Calculate the delta
delta = total_income - total_spent

# Get the transactions for the previous timeframe
prev_category_transactions_df = get_transactions_by_category_between_dates(prev_start_date, prev_end_date)
prev_total_spent = prev_category_transactions_df['TotalSpent'].sum()

prev_income_query = f"""
    SELECT 
        SUM(cr.Amount) AS TotalIncome
    FROM cleaned_records AS cr
    WHERE (cr.Date >= '{prev_start_date}' AND cr.Date < '{prev_end_date}')
    AND cr.Amount > 0
"""

prev_income_result = get_dataframe_from_query(prev_income_query, database)
prev_total_income = prev_income_result['TotalIncome'].values[0]

prev_delta = prev_total_income - prev_total_spent

# Display the total income and delta
col1, col2, col3 = st.columns(3)


with col1:
    st.metric("Total Income", f"${total_income:,.2f}", delta=f"{rate_of_change(total_income, prev_total_income):.2f}%")
with col2:
    st.metric("Total Spent", f"${total_spent:,.2f}", delta=f"{rate_of_change(total_spent, prev_total_spent):.2f}%", delta_color="inverse")
with col3:
    st.metric("Delta", f"${delta:,.2f}", delta= f"{rate_of_change(delta, prev_delta):.2f}%")

# Create a bar chart for total spent by category
fig = px.bar(category_transactions_df, x='CategoryName', y='TotalSpent', title='Total Spent by Category')
st.plotly_chart(fig)

# Create a pie chart for total spent by category
fig = px.pie(category_transactions_df, values='TotalSpent', names='CategoryName', title='Total Spent by Category')
st.plotly_chart(fig)

entity_transactions_df = get_transactions_by_entity_between_dates(start_date, end_date)

fig = px.bar(entity_transactions_df.set_index("EntityName")['TotalSpent'], title='Total Spent by Entity')
st.plotly_chart(fig)

fig = px.pie(entity_transactions_df, values='TotalSpent', names='EntityName', title='Total Spent by Entity')
st.plotly_chart(fig)


