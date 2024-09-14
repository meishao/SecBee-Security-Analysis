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
'''

import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

dashboard = st.Page(
    "dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True
)
bugs = st.Page("reports/bugs.py", title="Bug reports", icon=":material/bug_report:")
alerts = st.Page(
    "reports/alerts.py", title="System alerts", icon=":material/notification_important:"
)

search = st.Page("tools/search.py", title="Search", icon=":material/search:")
history = st.Page("tools/history.py", title="History", icon=":material/history:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard, bugs, alerts],
            "Tools": [search, history],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
