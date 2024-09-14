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

def login():
    st.title("登录")

    # 创建左右两列布局
    col1, col2 = st.columns([1, 1])  # 您可以调整比例，如 [1, 2]

    with col1:
        # 在左侧列添加图片
        st.image("logo.png", caption="欢迎使用 SecBee AI 安全分析", use_column_width=True)
        # 请将 "path_to_your_image.jpg" 替换为您的图片路径或 URL

    with col2:
        # 在右侧列添加登录表单
        st.subheader("登录您的账户")

        email = st.text_input("邮箱")
        password = st.text_input("密码", type="password")

        if st.button("登录"):
            try:
                # 使用 Supabase 客户端进行认证
                auth_response = supabase.client.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                if auth_response.user:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = auth_response.user
                    st.success("登录成功")
                else:
                    st.error("登录失败，请检查您的邮箱和密码。")
            except Exception as e:
                st.error(f"登录时出错：{e}")

def logout():
    st.title("退出登录")
    if st.button("退出"):
        # 使用 Supabase 客户端进行登出
        supabase.client.auth.sign_out()
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.success("已成功退出登录")

# 定义页面
dashboard = st.Page(
    "dashboard.py", title="仪表板", icon=":material/dashboard:", default=True
)
top_country_threat = st.Page(
    "pages/top_country_threat.py", title="全球威胁趋势", icon=":material/bug_report:"
)
top_threat_category = st.Page(
    "pages/top_threat_category.py", title="威胁分类排行", icon=":material/notification_important:"
)
search = st.Page("pages/snort_rule.py", title="搜索", icon=":material/search:")
history = st.Page("pages/admin.py", title="历史记录", icon=":material/history:")

# 导航
if st.session_state.get("logged_in"):
    pg = st.navigation(
        {
            "账户": [st.Page(logout, title="退出登录", icon=":material/logout:")],
            "报告": [dashboard, top_country_threat, top_threat_category],
            "工具": [search, history],
        }
    )
else:
    pg = st.navigation(
        {
            "账户": [st.Page(login, title="登录", icon=":material/login:")],
        }
    )

pg.run()
