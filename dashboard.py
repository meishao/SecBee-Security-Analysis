import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data as vega_data  # Vega datasets include geographic data for Altair

st.title("SecBee AI Security Analysis")
uploaded_file = st.file_uploader("Upload analysis file:")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    # Preview the raw data in an expander
    with st.expander("Data preview"):
        st.write(data)

    # Automatically identify the column names
    column_names = data.columns.tolist()
    country_col = column_names[0]  # Assuming the first column is the country
    count_col = column_names[1]  # Assuming the second column is the count

    # Clean the count column by removing commas and converting to integers
    data[count_col] = data[count_col].str.replace(',', '').astype(int)

    # Sort the data by the count column in descending order
    data = data.sort_values(by=count_col, ascending=False)

    # Select countries to display using a filter
    selected_countries = st.multiselect(
        "Select countries to include:",
        options=data[country_col].unique(),
        default=data[country_col].unique()
    )

    # Filter the data based on the selected countries
    filtered_data = data[data[country_col].isin(selected_countries)]

    # Load world map data from Altair's vega_datasets
    countries = alt.topo_feature(vega_data.world_110m.url, 'countries')

    # Create the map chart
    map_chart = alt.Chart(countries).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).properties(
        width=800,
        height=400
    ).project('mercator')

    # Create the bubble chart based on filtered data
    points = alt.Chart(filtered_data).mark_circle().encode(
        longitude='Longitude:Q',  # Assumes you have a column with longitude data
        latitude='Latitude:Q',    # Assumes you have a column with latitude data
        size=alt.Size(f'{count_col}:Q', title='Count of Records', scale=alt.Scale(range=[10, 1000])),  # Size of the bubbles
        color=alt.Color(f'{count_col}:Q', scale=alt.Scale(scheme='reds'), title='Count of Records'),
        tooltip=[country_col, count_col]
    )

    # Combine the map and the points (bubbles)
    final_chart = map_chart + points

    # Display the map in Streamlit
    st.altair_chart(final_chart, use_container_width=True)
