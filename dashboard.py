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
    # Convert the count column to numeric (removing commas if present)
    data['Count of records'] = data['Count of records'].str.replace(',', '').astype(int)

    # Set the threat categories as the index
    data.set_index('Top 200 values of sourceClass.keyword', inplace=True)

    # Plot the bar chart using st.bar_chart
    st.bar_chart(data['Count of records'])



