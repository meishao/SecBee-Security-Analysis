import streamlit as st
import pandas as pd

st.title("SecBee AI Security Analysis")
uploaded_file = st.file_uploader("Upload analysis file:")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    with st.expander("Data preview"):
        st.write(dataframe)

if st.button("Start"):
    st.write("Analyzing...")
    #st.write(dataframe)

st.bar_chart(dataframe, x="Count of records", y="Top 200 values of sourceClass.keyword", color="site", horizontal=True)

