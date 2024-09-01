import pandas as pd
import plotly.express as px
import streamlit as st

from commands.add_record_if_new import add_record_if_new
from commands.get_all_from_table_where import get_all_from_table_where
from commands.get_database_tables import get_database_tables
from commands.get_list_of_values_from_column import get_list_of_values_from_column
from commands.remove_from_table import remove_from_table

database = 'finances_db'
table_name = 'cleaned_records'

if table_name in get_database_tables(database, clean=True):
    with st.expander("Entities"):
        entities = pd.read_sql_query(f"SELECT DISTINCT Entity FROM {table_name}", f"sqlite:///{database}.db")
        df = pd.DataFrame(entities)
        st.dataframe(df, use_container_width=True, hide_index=True)

    with st.expander("Manager an Entity"):
        entity_name = st.selectbox("Select an Entity", entities['Entity'])
        st.subheader("Associations")
        if "entity_category" in get_database_tables(database, clean=True):
            where_str = f"entity_name = '{entity_name}'"
            columns_str = "entity_name, category_name"
            associations = pd.read_sql_query(f"SELECT category_name FROM entity_category WHERE entity_name = '{entity_name}';", f"sqlite:///{database}.db")
            df = pd.DataFrame(associations)
            st.write("Existing Entity to Category Associations")
            st.dataframe(df, use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2, gap="large", vertical_alignment="bottom")
        with col1:
            category_names = get_list_of_values_from_column(database, 'categories', 'Name')
            category_name = st.selectbox("Select an Category to associate this Entity with:", category_names, key="association_select")
        with col2:
            associate_button = st.button("Associate", key='associate_button')

            if associate_button:
                record = {'entity_name': entity_name, 'category_name': category_name}
                df = pd.DataFrame([record])
                if "entity_category" not in get_database_tables(database, clean=True):
                    existing = False
                else:
                    where_str = f"entity_name = '{entity_name}' AND category_name = '{category_name}'"
                    existing = get_all_from_table_where(database, 'entity_category', where_str)
                if not existing:
                    add_record_if_new(database, 'entity_category', df)
                st.success(f"{entity_name} associated with {category_name} successfully!")
                st.rerun()

        col1, col2 = st.columns(2, gap="large", vertical_alignment="bottom")
        with col1:
            asc_categories = pd.read_sql_query(f"SELECT category_name FROM entity_category WHERE entity_name = '{entity_name}';", f"sqlite:///{database}.db")
            df = pd.DataFrame(asc_categories)
            asc_category_names = df['category_name'].unique().tolist()
            asc_category_name = st.selectbox("Select an Category to associate this Entity with:", asc_category_names, key="remove_association_select")
        with col2:
            disassociate_button = st.button("Remove Association", key='remove_association_button')

            if disassociate_button:
                record = {'entity_name': entity_name, 'category_name': asc_category_name}
                df = pd.DataFrame([record])
                where_str = f"entity_name = '{entity_name}' AND category_name = '{asc_category_name}'"
                remove_from_table(database, 'entity_category', 'entity_name', None, where_str=where_str)
                st.success(f"{entity_name} association with {asc_category_name} removed successfully!")

    with st.expander("Analysis"):
        entity_name = st.selectbox("Select an Entity", entities['Entity'], key="analysis_select")
        # Filter by dates
        start_date = st.date_input("Start Date", format="YYYY/MM/DD", value=pd.to_datetime("2023/01/01"))
        end_date = st.date_input("End Date", format="YYYY/MM/DD")
        
        query = f"SELECT * FROM {table_name} WHERE Entity = '{entity_name}' AND (Date >= '{start_date}' AND Date < '{end_date}')"
        transactions_df = pd.read_sql_query(query, f"sqlite:///{database}.db")
        st.dataframe(transactions_df, use_container_width=True, hide_index=True)
        
        total_spend = transactions_df['Amount'].sum() * -1
        st.metric("Total Spent", f"${total_spend:,.2f}")

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
        spend_over_time = transactions_df.groupby('Time Group')['Amount'].sum().abs()

        # Plot line chart with trendline
        fig = px.line(spend_over_time, title="Spend Over Time", markers=True, labels={'Time Group': 'Time Group', 'Amount': 'Amount'})
        mean = spend_over_time.mean()
        fig.add_hline(y=mean, line_dash="dash", line_color="red", annotation_text=f"Average | ${mean:,.2f}", annotation_position="bottom right")
        st.plotly_chart(fig)
        