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

    # Create a bar chart
    fig, ax = plt.subplots()
    ax.barh(data['Top 200 values of sourceClass.keyword'], data['Count of records'])
    ax.set_xlabel('Count of Records')
    ax.set_ylabel('Threat Categories')
    ax.set_title('Top 200 Threat Categories by Record Count')

    # Display the chart in Streamlit
    st.pyplot(fig)



