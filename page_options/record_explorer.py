import pandas as pd
import plotly.express as px
import streamlit as st

from commands.add_record_if_new import add_record_if_new
from commands.get_all_from_table_where import get_all_from_table_where
from commands.get_database_tables import get_database_tables
from commands.get_list_of_values_from_column import get_list_of_values_from_column
from commands.remove_from_table import remove_from_table
from modules.toolbox import snake_case


database = 'finances_db'
table_name = 'cleaned_records'

if table_name in get_database_tables(database, clean=True):
    with st.expander("Analysis", expanded=True):
        # Filter by dates
        start_date = st.date_input("Start Date", format="YYYY/MM/DD", value=pd.to_datetime("2023/01/01"))
        end_date = st.date_input("End Date", format="YYYY/MM/DD")

        query = f"""
                SELECT 
                    ce.Amount,
                    ce.Date,
                    ce.Entity,
                    ec.category_name,
                    ce.TransactionId        
                FROM cleaned_records ce 
                INNER JOIN entity_category ec ON ce.Entity = ec.entity_name
                WHERE ce.Date >= '{start_date}' AND ce.Date < '{end_date}'"""

        transactions_df = pd.read_sql_query(query, f"sqlite:///{database}.db")
        st.dataframe(transactions_df, use_container_width=True, hide_index=True)

        st.subheader("Overview")

        total_spend = transactions_df.loc[transactions_df['Amount'] < 0, 'Amount'].sum() * -1
        total_income = transactions_df.loc[transactions_df['Amount'] > 0, 'Amount'].sum()
        delta = total_income - total_spend
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Income", f"${total_income:,.2f}")
        with col2:
            st.metric("Total Spend", f"${total_spend:,.2f}")
        with col3:
            st.metric("Delta", f"${delta:,.2f}")

        top_20_spend_df = transactions_df.loc[transactions_df['Amount'] < 0].copy()
        top_20_spend_df['Amount'] *= -1
        st.dataframe(top_20_spend_df, use_container_width=True, hide_index=True)
        top_20_spend_df = top_20_spend_df.groupby('Entity')['Amount'].sum().nlargest(20).reset_index()

        fig = px.pie(top_20_spend_df, names='Entity', values='Amount', title="Top 20 Expenses")
        st.plotly_chart(fig)

        # Group by selected time units
        time_units = st.selectbox("Group by", ["Day", "Week", "Month", "Quarter", "Year"])
        if time_units == "Day":
            transactions_df['Time Group'] = pd.to_datetime(transactions_df['Date']).dt.date
        elif time_units == "Week":
            transactions_df['Time Group'] = pd.to_datetime(transactions_df['Date']).dt.to_period('W').apply(lambda x: x.start_time)
        elif time_units == "Month":
            transactions_df['Time Group'] = pd.to_datetime(transactions_df['Date']).dt.to_period('M').apply(lambda x: x.start_time)
        elif time_units == "Quarter":
            transactions_df['Time Group'] = pd.to_datetime(transactions_df['Date']).dt.to_period('Q').apply(lambda x: x.start_time)
        elif time_units == "Year":
            transactions_df['Time Group'] = pd.to_datetime(transactions_df['Date']).dt.to_period('Y').apply(lambda x: x.start_time)

        # Calculate spend over time
        spend_over_time = transactions_df.groupby('Time Group')['Amount'].sum()

        # Plot line chart with trendline
        fig = px.line(spend_over_time, title="Net Income Over Time", markers=True, labels={'Time Group': 'Time Group', 'Amount': 'Amount'})
        avg_line = spend_over_time.mean()
        fig.add_hline(y=avg_line, line_dash="dash", line_color="red", annotation_text=f"Average: {avg_line:.2f}", annotation_position="bottom right")
        st.plotly_chart(fig)

        
