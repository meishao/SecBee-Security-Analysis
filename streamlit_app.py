import streamlit as st
import streamlit.components.v1 as components
from st_supabase_connection import SupabaseConnection
from app_pages.login import login_page
from time import sleep

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
    logout_page = st.Page(logout, title="退出登录", icon=":material/logout:")

    # 导航
    pg = st.navigation(
        {
            "账号": [logout_page],
            "报告": [admin_page, top_country_threat_page, top_threat_category_page],
            "工具": [search_page, history_page],
        }
    )

    pg.run()

def logout():
    # 使用 Supabase 进行登出
    supabase.auth.sign_out()
    st.session_state.clear()
    sleep(0.5)
    # 创建一个包含meta标签的HTML代码，设置页面跳转
    html_code = """
    <html>
    <head>
        <meta http-equiv="refresh" content="1; url=https://secbee.streamlit.app/">
    </head>
    <body>
        <p>如果页面没有自动跳转，请 <a href="https://secbee.streamlit.app/">点击这里</a>。</p>
    </body>
    </html>
    """
    # 使用 components.v1.html() 嵌入 HTML 代码
    components.html(html_code)

def main():
    if not check_auth():
        login_page(supabase)
    else:
        dashboard()

if __name__ == "__main__":
    main()
    
