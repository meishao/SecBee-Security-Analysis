import streamlit as st
from st_supabase_connection import SupabaseConnection
from app_pages.login import login_page
from app_pages.dashboard import dashboard_page

# 初始化 Supabase 连接
def init_supabase_connection():
    return SupabaseConnection(connection_name="supabase")

supabase = init_supabase_connection()

def check_auth():
    return 'user' in st.session_state

def dashboard():
    admin_page = st.Page(
        "app_pages/super-admin.py", title="仪表板", icon=":material/dashboard:", default=True
    )
    top_country_threat_page = st.Page(
        "app_pages/top_country_threat.py", title="全球威胁趋势", icon=":material/bug_report:"
    )
    top_threat_category_page = st.Page(
        "app_pages/top_threat_category.py", title="威胁分类排行", icon=":material/notification_important:"
    )
    search_page = st.Page("app_pages/snort_rule.py", title="搜索", icon=":material/search:")
    history_page = st.Page("app_pages/admin.py", title="历史记录", icon=":material/history:")
    logout_page = st.Page(logout(supabase), title="退出登录", icon=":material/logout:")

    # 导航
    pg = st.navigation(
        {
            "账号": [logout_page],
            "报告": [dashboard_page, top_country_threat_page, top_threat_category_page],
            "工具": [search_page, history_page],
        }
    )

    pg.run()

def logout():

def main():
    if not check_auth():
        login_page()
    else:
        dashboard()

if __name__ == "__main__":
    main()
    
