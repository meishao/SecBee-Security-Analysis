import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data as vega_data

# Load the country coordinates from the uploaded file
country_coords = pd.read_csv('data/countries.csv')

st.title("SecBee AI Security Analysis")

# Upload the user's data (with country and count columns)
uploaded_file = st.file_uploader("Upload analysis file:")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Preview the raw data
    with st.expander("Data preview"):
        st.write(data)

    # Automatically identify the column names
    column_names = data.columns.tolist()
    country_col = column_names[0]  # Assuming the first column is the country name
    count_col = column_names[1]  # Assuming the second column is the count

    # Clean the count column by removing commas and converting to integers
    data[count_col] = data[count_col].str.replace(',', '').astype(int)

    # Merge the user data with the country coordinates based on country name
    merged_data = pd.merge(data, country_coords, left_on=country_col, right_on='name', how='inner')

    # Sort the data by the count column in descending order
    merged_data = merged_data.sort_values(by=count_col, ascending=False)

    # Select countries to display using a filter
    selected_countries = st.multiselect(
        "Select countries to include:",
        options=merged_data['name'].unique(),
        default=merged_data['name'].unique()
    )

    # Filter the data based on the selected countries
    filtered_data = merged_data[merged_data['name'].isin(selected_countries)]

    ### Display the Bar Chart ###
    st.header("Bar Chart of Threat Counts by Country")
    bar_chart = alt.Chart(filtered_data).mark_bar().encode(
        x=alt.X(f'{count_col}:Q', title='Count of Records'),
        y=alt.Y('name:N', sort='-x', title='Country')
    ).properties(
        width=700,
        height=400
    )
    st.altair_chart(bar_chart, use_container_width=True)

    ### Display the World Map ###
    st.header("World Map of Threat Counts by Country")
    # Load world map data from Altair's vega_datasets
    countries = alt.topo_feature(vega_data.world_110m.url, 'countries')

    # Create the map chart with improved projection and aspect ratio
    map_chart = alt.Chart(countries).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).properties(
        width=1000,
        height=600
    ).project('equirectangular')  # Equirectangular projection for full globe view

    # Create the bubble chart based on filtered data
    points = alt.Chart(filtered_data).mark_circle().encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        size=alt.Size(f'{count_col}:Q', title='Count of Records', scale=alt.Scale(range=[10, 1000])),
        color=alt.Color(f'{count_col}:Q', scale=alt.Scale(scheme='reds'), title='Count of Records'),
        tooltip=['name', count_col]
    )

    # Combine the map and the points (bubbles)
    final_chart = map_chart + points

    # Display the map in Streamlit
    st.altair_chart(final_chart, use_container_width=True)
