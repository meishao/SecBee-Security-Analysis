import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("SecBee AI Security Analysis")
uploaded_file = st.file_uploader("Upload analysis file:")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    with st.expander("Data preview"):
        st.write(data)

if st.button("Start"):
    st.write("Analyzing...")
    #st.write(dataframe)
    #data['Count of records'] = data['Count of records'].str.replace(',', '').astype(int)
    st.bar_chart(data.set_index('sourceClass'), horizontal=True)



