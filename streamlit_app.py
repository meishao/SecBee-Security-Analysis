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
top_country_threat = st.Page("pages/top_country_threat.py", title="全球威胁趋势", icon=":material/bug_report:")
top_threat_category = st.Page(
    "pages/top_threat_category.py", title="威胁分类排行", icon=":material/notification_important:"
)

search = st.Page("pages/snort_rule.py", title="Search", icon=":material/search:")
history = st.Page("pages/admin.py", title="History", icon=":material/history:")

if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Reports": [dashboard, top_country_threat, top_threat_category],
            "Tools": [search, history],
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()

'''

import streamlit as st
from st_supabase_connection import SupabaseConnection

# 初始化 Supabase 连接
@st.cache_resource
def init_supabase_connection():
    #return SupabaseConnection(connection_name="supabase", type=SupabaseConnection)
    conn = st.connection("supabase",type=SupabaseConnection)
    return conn

supabase = init_supabase_connection()

# 初始化 session_state 变量
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None

def login():
    st.title("登录")

    email = st.text_input("邮箱")
    password = st.text_input("密码", type="password")

    if st.button("登录"):
        try:
            # 使用 st-supabase-connection 进行认证
            user = supabase.login(email, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.success("登录成功")
                st.experimental_rerun()
            else:
                st.error("登录失败，请检查您的邮箱和密码。")
        except Exception as e:
            st.error(f"登录时出错：{e}")

def logout():
    st.title("退出登录")
    if st.button("退出"):
        # 使用 st-supabase-connection 进行登出
        supabase.logout()
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.success("已成功退出登录")
        st.experimental_rerun()

# 定义页面
dashboard = st.Page(
    "dashboard.py", title="仪表板", icon=":material-dashboard:", default=True
)
top_country_threat = st.Page(
    "pages/top_country_threat.py", title="全球威胁趋势", icon=":material-bug-report:"
)
top_threat_category = st.Page(
    "pages/top_threat_category.py", title="威胁分类排行", icon=":material-notification-important:"
)
search = st.Page("pages/snort_rule.py", title="搜索", icon=":material-search:")
history = st.Page("pages/admin.py", title="历史记录", icon=":material-history:")

# 导航
if st.session_state["logged_in"]:
    pg = st.navigation(
        {
            "账户": [st.Page(logout, title="退出登录", icon=":material-logout:")],
            "报告": [dashboard, top_country_threat, top_threat_category],
            "工具": [search, history],
        }
    )
else:
    pg = st.navigation(
        {
            "账户": [st.Page(login, title="登录", icon=":material-login:")],
        }
    )

pg.run()

