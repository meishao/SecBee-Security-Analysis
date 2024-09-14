import streamlit as st
import pandas as pd
import altair as alt

st.title("SecBee AI Security Analysis")
uploaded_file = st.file_uploader("Upload analysis file:")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    
    # Preview the raw data in an expander
    with st.expander("Data preview"):
        st.write(data)

    # Automatically identify the column names
    column_names = data.columns.tolist()
    category_col = column_names[0]  # Assuming the first column is the category
    count_col = column_names[1]  # Assuming the second column is the count

    # Clean the count column by removing commas and converting to integers
    data[count_col] = data[count_col].str.replace(',', '').astype(int)

    # Sort the data by the count column in descending order
    data = data.sort_values(by=count_col, ascending=False)

    # Dynamic filter for Y-axis categories
    selected_categories = st.multiselect(
        "Select categories to include:",
        options=data[category_col].unique(),
        default=data[category_col].unique()
    )

    # Filter the data based on the selected categories
    filtered_data = data[data[category_col].isin(selected_categories)]

    # Create a horizontal bar chart using Altair
    chart = alt.Chart(filtered_data).mark_bar().encode(
        x=alt.X(f'{count_col}:Q', title='Count of Records'),
        y=alt.Y(f'{category_col}:N', sort='-x', 
                title='Threat Category', 
                axis=alt.Axis(
                    titleAnchor="start",  # Move Y-axis title to the left
                    titleAngle=0,  # Ensure title is horizontal
                    labelLimit=600,  # Limit label length
                    labelAngle=-30  # Rotate labels if needed
                ))
    ).properties(
        title=alt.TitleParams(
            text="Top Threat Categories by Count",  # Chart title
            offset=20,  # Adjust this value to avoid blocking
            fontSize=16  # Adjust font size if needed
        ),
        padding={"left": 100, "top": 30}  # Add padding on the left for Y-axis title
    )

    # Display the Altair chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
