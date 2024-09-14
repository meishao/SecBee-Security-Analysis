import streamlit as st
import pandas as pd
import altair as alt

st.title("SecBee AI Security Analysis")
uploaded_file = st.file_uploader("Upload analysis file:")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    with st.expander("Data preview"):
        st.write(data)

if st.button("Start"):
    st.write("Analyzing...")
    #data['count'] = data['count'].str.replace(',', '').astype(int)
    #st.bar_chart(data.set_index('sourceClass'), horizontal=True)
    # Create a horizontal bar chart using Altair
    chart = alt.Chart(data).mark_bar().encode(
        x='Count of records:Q',
        y=alt.Y('sourceClass:N', sort='-x')  # Sort by the count of records in descending order
    ).properties(
        title="Top Threat Categories by Count"
    )

    # Display the Altair chart in Streamlit
    st.altair_chart(chart, use_container_width=True)


