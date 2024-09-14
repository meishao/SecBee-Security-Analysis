import streamlit as st
from st_supabase_connection import SupabaseConnection

# 初始化 Supabase 连接
@st.cache_resource
def init_supabase_connection():
    return SupabaseConnection(connection_name="supabase")

supabase = init_supabase_connection()

# 初始化 session_state 变量
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None

# 导入页面函数
from pages.login import login_page
from pages.dashboard import dashboard_page
from pages.logout import logout_page
# ... 导入其他页面

# 获取查询参数
page = st.query_params.page if "page" in st.query_params else "login"

# 页面导航逻辑
if page == "login":
    login_page(supabase)
elif page == "dashboard":
    if st.session_state.get("logged_in"):
        dashboard_page()
    else:
        st.warning("请先登录。")
        # 避免死循环，仅当查询参数需要修改时才进行更新和跳转
        if st.query_params.page != "login":
            st.query_params.page = "login"
            st.rerun()
elif page == "logout":
    logout_page(supabase)
else:
    if st.query_params.page != "login":
        st.query_params.page = "login"
        st.rerun()
