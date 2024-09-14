import streamlit as st
import pandas as pd

st.title("SecBee AI Security Analysis")
uploaded_file = st.file_uploader("Upload analysis file:")
if uploader_file is not None:
    dataframe = pd.read_csv(uploaded_file)

if st.button("Start"):
    st.write("Analyzing...")
    st.write(dataframe)
