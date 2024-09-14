import streamlit as st
import pandas as pd
import altair as alt

st.title("SecBee AI Security Analysis")

# Upload analysis file
uploaded_file = st.file_uploader("Upload analysis file:")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    # Data preview
    with st.expander("Data preview"):
        st.write(data)

    # List all column names
    column_names = data.columns.tolist()

    # Identify numerical and categorical columns
    numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns.tolist()

    st.subheader("Select Variables for Analysis")

    # Allow the user to select X-axis (numerical) and Y-axis (categorical) variables
    x_col = st.selectbox("Select X-axis variable (numerical):", options=column_names)
    y_col = st.selectbox("Select Y-axis variable (categorical):", options=column_names)

    # Initialize session state for START button
    if 'start_clicked' not in st.session_state:
        st.session_state['start_clicked'] = False

    # Layout for START and Reset buttons
    col_start, col_reset = st.columns([1, 1])
    with col_start:
        if st.button("START"):
            st.session_state['start_clicked'] = True
    with col_reset:
        if st.button("Reset"):
            st.session_state['start_clicked'] = False

    # Proceed if START has been clicked
    if st.session_state['start_clicked']:
        # Clean the X-axis column (remove commas and convert to numeric)
        data[x_col] = data[x_col].astype(str).str.replace(',', '').astype(float)

        # Sort data descending by the X-axis variable
        data = data.sort_values(by=x_col, ascending=False)

        # Create left and right columns
        col1, col2 = st.columns([1, 3])  # Left column is 1, right column is 3

        # Left column: filter selection
        with col1:
            selected_categories = st.multiselect(
                "Select categories to include:",
                options=data[y_col].unique(),
                default=data[y_col].unique()
            )

        # Filter data based on selected categories
        filtered_data = data[data[y_col].isin(selected_categories)]

        # Right column: create horizontal bar chart
        with col2:
            chart = alt.Chart(filtered_data).mark_bar().encode(
                x=alt.X(f'{x_col}:Q', title=x_col),
                y=alt.Y(f'{y_col}:N', sort='-x',
                        title=y_col,
                        axis=alt.Axis(
                            titleAnchor="start",
                            titleAngle=0,
                            labelLimit=600,
                        ))
            ).properties(
                title=alt.TitleParams(
                    text=f"Top {y_col} by {x_col}",
                    offset=20,
                    fontSize=16
                ),
                padding={"left": 30, "top": 30}
            )

            # Display the chart in Streamlit
            st.altair_chart(chart, use_container_width=True)
