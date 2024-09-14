import streamlit as st
from st_supabase_connection import SupabaseConnection

# 初始化 Supabase 连接
@st.cache_resource
def init_supabase_connection():
    return SupabaseConnection(connection_name="supabase")

supabase = init_supabase_connection()

# 导入页面函数
from pages.login import login_page
from pages.dashboard import dashboard_page
from pages.logout import logout_page
# ... 导入其他页面

def check_auth():
    return 'user' in st.session_state

def main():
    if not check_auth():
        login()
    else:
        dashboard()

if __name__ == "__main__":
    main()
