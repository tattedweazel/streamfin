import streamlit as st

def display_empty_lines(num_lines: int):
    for _ in range(num_lines):
        st.write("\n")