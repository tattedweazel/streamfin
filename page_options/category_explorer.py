import pandas as pd
import plotly.express as px
import streamlit as st

from commands.add_record_if_new import add_record_if_new
from commands.get_all_from_table_where import get_all_from_table_where
from commands.get_database_tables import get_database_tables
from commands.get_dataframe_from_query import get_dataframe_from_query
from commands.get_list_of_values_from_column import get_list_of_values_from_column
from commands.remove_from_table import remove_from_table
from modules.toolbox import snake_case


database = 'finances_db'
table_name = 'categories'


if "categories" in get_database_tables(database, clean=True):
    with st.expander("Categories"):
        categories = pd.read_sql_query(f"SELECT category_name as Name, count(*) as Entities FROM entity_category GROUP BY 1 ORDER BY 2 desc", f"sqlite:///{database}.db")
        categories_df = pd.DataFrame(categories)
        st.dataframe(categories_df, use_container_width=True, hide_index=True)

    with st.expander("Manager a Category"):
        category_name = st.selectbox("Select a Category", categories['Name'])
        delete_button = st.button("Delete")

        if delete_button:
            remove_from_table(database, table_name, 'Name', category_name)
            st.success(f"Category {category_name} deleted successfully!")
            st.rerun()

        st.subheader("Associations")
        if "entity_category" in get_database_tables(database, clean=True):
            where_str = f"category_name = '{category_name}'"
            columns_str = "entity_name, category_name"
            associations = get_all_from_table_where(database, 'entity_category', where_str, columns_str)
            df = pd.DataFrame(associations)
            st.write("Existing Entity to Category Associations")
            st.dataframe(df, use_container_width=True)


        col1, col2 = st.columns(2, gap="large", vertical_alignment="bottom")
        with col1:
            entity_names = get_list_of_values_from_column(database, 'transform_pattern', 'clean_description')
            entity_name = st.selectbox("Select an Entity to associate this Category with:", entity_names)
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
                st.success(f"Entity {entity_name} associated with Category {category_name} successfully!")
                st.rerun()


with st.expander("Add a Category"):
    category_name = st.text_input("Category Name")
    submit_button = st.button("Submit")

    if submit_button:
        if category_name.strip() == "":
            st.warning("Category Name cannot be blank.")
            st.stop()
        record = {'Name': category_name}
        df = pd.DataFrame([record])
        existing = get_all_from_table_where(database, table_name, where_str = f"Name = '{category_name}'", columns_str="Name")
        if not existing:
            add_record_if_new(database, table_name, df)
        st.success(f"Category {category_name} added successfully!")
        st.rerun()
        

with st.expander("Brute Force Category Association"):
    associated_entities = get_list_of_values_from_column(database, 'entity_category', 'entity_name')
    all_entities = get_list_of_values_from_column(database, 'transform_pattern', 'clean_description')
    missing_entities = list(set(all_entities) - set(associated_entities))
    st.write("Entities Missing Association:")
    for entity in missing_entities:
        col1, col2, col3 = st.columns(3, gap="medium", vertical_alignment="bottom")
        with col1:
            st.info(entity)
        with col2:
            category_name = st.selectbox("Select a Category", categories['Name'], key=f"{snake_case(entity)}_select")
        with col3:
            associate_button = st.button("Associate", key=f"{snake_case(entity)}_associate")
            if associate_button:
                record = {'entity_name': entity, 'category_name': category_name}
                df = pd.DataFrame([record])
                add_record_if_new(database, 'entity_category', df)
                st.success(f"Entity {entity} associated with Category {category_name} successfully!")
                st.rerun()

with st.expander("Export current categories"):
    export_button = st.button("Export to CSV")

    if export_button:
        # Get all records from entity_category table
        entity_category_df = get_dataframe_from_query("SELECT entity_name, category_name FROM entity_category", database)

        # Define export file path
        export_file_path = 'exports/entity_category.csv'

        # Export DataFrame to CSV
        entity_category_df.to_csv(export_file_path, index=False)

        st.success("Exported to CSV successful!")

with st.expander("Analysis"):
        category_name = st.selectbox("Select an Category", categories_df['Name'], key="analysis_select")
        # Filter by dates
        start_date = st.date_input("Start Date", format="YYYY/MM/DD", value=pd.to_datetime("2023/01/01"))
        end_date = st.date_input("End Date", format="YYYY/MM/DD")

        query = f"""
            SELECT
                ec.category_name,
                ce.Entity, 
                ce.Amount,
                ce.Date
            FROM cleaned_records ce 
            INNER JOIN entity_category ec ON ce.Entity = ec.entity_name
            WHERE ec.category_name = '{category_name}' 
            AND (ce.Date >= '{start_date}' AND ce.Date < '{end_date}')
            """

        transactions_df = pd.read_sql_query(query, f"sqlite:///{database}.db")
        grouped_df = transactions_df.groupby('Entity')['Amount'].sum().abs()
        st.dataframe(grouped_df, use_container_width=True)
        total_spend = transactions_df['Amount'].sum() * -1
        st.metric("Total Spent", f"${total_spend:,.2f}")

        # Calculate total spend by entity
        total_spend_by_entity = transactions_df.groupby('Entity')['Amount'].sum().abs()

        # Plot pie chart of total spend by entity
        fig = px.pie(total_spend_by_entity, values='Amount', names=total_spend_by_entity.index, title='Total Spend by Entity')
        st.plotly_chart(fig)
