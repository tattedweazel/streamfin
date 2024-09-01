import streamlit as st
import pandas as pd
import os


st.title("CSV File Uploader")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Check if the uploaded file is a CSV file
    if uploaded_file.type == 'text/csv':
        # Store the uploaded file to a local directory
        file_path = os.path.join('uploads', uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Read the CSV file
        df = pd.read_csv(file_path, header=0)
        
        # Display the uploaded data
        st.dataframe(df)
        
        # Store the data in a database or perform any other operations
        
        st.success("File uploaded successfully!")
    else:
        st.error("Please upload a CSV file.")

# Get the list of CSV files in the "/uploads" folder
csv_files = [file for file in os.listdir('uploads') if file.endswith('.csv')]

# Display the list of CSV files
st.subheader("Existing CSV Files")
for file in csv_files:
    st.info(file)

# Delete CSV files
if csv_files:
    st.subheader("Existing CSV Files")
    df_files = pd.DataFrame(csv_files, columns=["File Name"])
    st.table(df_files)

    selected_file = st.selectbox("Select a file to delete", csv_files)
    delete_button = st.button("Delete File")

    if delete_button:
        file_path = os.path.join('uploads', selected_file)
        os.remove(file_path)
        st.success(f"{selected_file} has been deleted.")
else:
    st.subheader("No CSV Files Found")
