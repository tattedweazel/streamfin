import streamlit as st
import pandas as pd
import os

# Get the list of CSV files in the "uploads" folder
csv_files = [file for file in os.listdir("uploads") if file.endswith(".csv")]

# Create a collapsible list of CSV files
selected_csv = st.selectbox("Select a CSV file", csv_files)

# Read the selected CSV file
if selected_csv:
    csv_path = os.path.join("uploads", selected_csv)
    df = pd.read_csv(csv_path)

    # Display the tabular view of the CSV file
    st.dataframe(df, use_container_width=True)

else:
    st.write("No CSV file selected.")