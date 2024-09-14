'''
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
'''

import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

st.set_page_config(layout="wide")

# sections = st.sidebar.toggle("Sections", value=True, key="use_sections")

nav = get_nav_from_toml(".streamlit/pages_sections.toml")

# nav = get_nav_from_toml(
#    ".streamlit/pages_sections.toml" if sections else ".streamlit/pages.toml"
#)

st.logo("secbee-high-resolution-logo-transparent.png")

pg = st.navigation(nav)

add_page_title(pg)

pg.run()
