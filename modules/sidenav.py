import streamlit as st

def get_sidebar():

    # --- Pages ---
    default_page = st.Page(
        page='page_options/default.py',
        title='Home',
        url_path='/',
        icon=':material/view_cozy:',
        default=True
    )

    import_page = st.Page(
        page='page_options/csv_importer.py',
        title='Import CSV',
        url_path='/csv_import',
        icon=':material/cloud_upload:'
    )

    csv_explorer_page = st.Page(
        page='page_options/csv_explorer.py',
        title='CSV Explorer',
        url_path='/csv_explorer',
        icon=':material/text_snippet:'
    )

    database_page = st.Page(
        page='page_options/database_manager.py',
        title='Database Manager',
        url_path='/database_manager',
        icon=':material/database:'
    )

    data_loader_page = st.Page(
        page='page_options/data_loader.py',
        title='Load CSVs to Database',
        url_path='/data_loader',
        icon=':material/download_for_offline:'
    )

    data_transformer_page = st.Page(
        page='page_options/data_transformer.py',
        title='Data Transformer',
        url_path='/data_transformer',
        icon=':material/other_admission:'
    )

    table_explorer_page = st.Page(
        page='page_options/table_explorer.py',
        title='Table Explorer',
        url_path='/table_explorer',
        icon=':material/explore:'
    )

    pattern_explorer_page = st.Page(
        page='page_options/pattern_manager.py',
        title='Pattern Explorer',
        url_path='/pattern_manager',
        icon=':material/page_info:'
    )

    quicklook_page = st.Page(
        page='page_options/quicklook.py',
        title='Quick Look',
        url_path='/quicklook',
        icon=':material/visibility:'
    )

    spend_by_entity_page = st.Page(
        page='page_options/spend_by_entity.py',
        title='Spend by Entity',
        url_path='/spend_by_entity',
        icon=':material/monetization_on:'
    )

    spend_by_category_page = st.Page(
        page='page_options/spend_by_category.py',
        title='Spend by Category',
        url_path='/spend_by_category',
        icon=':material/currency_exchange:'
    )

    category_explorer_page = st.Page(
        page='page_options/category_explorer.py',
        title='Category Explorer',
        url_path='/category_explorer',
        icon=':material/category:'
    )

    entity_explorer_page = st.Page(
        page='page_options/entity_explorer.py',
        title='Entity Explorer',
        url_path='/entity_explorer',
        icon=':material/emoji_people:'
    )

    record_explorer_page = st.Page(
        page='page_options/record_explorer.py',
        title='Record Explorer',
        url_path='/record_explorer',
        icon=':material/insert_drive_file:'
    )

    pg = st.navigation(
        {
            "Main": [default_page],
            "ETL": [import_page, data_loader_page, data_transformer_page],
            "Explore": [csv_explorer_page, table_explorer_page, pattern_explorer_page, category_explorer_page, entity_explorer_page, record_explorer_page],
            "Reporting": [quicklook_page, spend_by_entity_page, spend_by_category_page],
            "Admin": [database_page]
        }
    )
    st.sidebar.text("It's going to be a good day!")
    return pg