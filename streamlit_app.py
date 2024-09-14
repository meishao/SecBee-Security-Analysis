import streamlit as st
from st_supabase_connection import SupabaseConnection

# 初始化 Supabase 连接
def init_supabase_connection():
    return SupabaseConnection(connection_name="supabase")

supabase = init_supabase_connection()

# 导入页面函数
from pages.login import login_page
from pages.dashboard import dashboard_page
# from pages.logout import logout_page
# ... 导入其他页面

def check_auth():
    return 'user' in st.session_state

def main():
    if not check_auth():
        login_page(supabase)
    else:
        dashboard_page()

if __name__ == "__main__":
    main()
