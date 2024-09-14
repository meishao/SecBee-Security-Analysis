import streamlit as st

def dashboard_page():
    # 检查用户是否已登录
    if not st.session_state.logged_in:
        st.warning("请先登录以访问此页面。")
        st.rerun()
    else:
        # 定义页面
        dashboard_page = st.Page(
            "pages/dashboard.py", title="仪表板", icon=":material/dashboard:", default=True
        )
        top_country_threat_page = st.Page(
            "pages/top_country_threat.py", title="全球威胁趋势", icon=":material/bug_report:"
        )
        top_threat_category_page = st.Page(
            "pages/top_threat_category.py", title="威胁分类排行", icon=":material/notification_important:"
        )
        search_page = st.Page("pages/snort_rule.py", title="搜索", icon=":material/search:")
        history_page = st.Page("pages/admin.py", title="历史记录", icon=":material/history:")
        logout_page = st.Page("pages/logout.py", title="退出登录", icon=":material/logout:")

        # 导航
        pg = st.navigation(
            {
                "账户": [logout_page],
                "报告": [dashboard_page, top_country_threat_page, top_threat_category_page],
                "工具": [search_page, history_page],
            }
        )

        pg.run()
