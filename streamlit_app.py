import streamlit as st
from st_supabase_connection import SupabaseConnection

# 设置页面配置
st.set_page_config(page_title="SecBee AI Security Analysis", page_icon=":lock:", layout="wide")

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
    # 移除默认的间距和边距，设置背景颜色
    st.markdown(
        """
        <style>
        /* 移除页面容器的默认间距 */
        div.block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        /* 设置背景颜色 */
        .stApp {
            background-color: #1E1E1E;
        }
        /* 输入框样式 */
        input {
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #555555;
        }
        /* 调整按钮样式 */
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            height: 45px;
            width: 100%;
            font-size: 16px;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        /* 居中登录表单 */
        .login-form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        /* 调整字体颜色 */
        h1, label {
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # 创建左右两列
    col1, col2 = st.columns(2)

    # 左侧列：Logo
    with col1:
        st.image('logo.png', use_column_width=True)

    # 右侧列：登录表单
    with col2:
        st.markdown("<div class='login-form'>", unsafe_allow_html=True)
        st.markdown("<h1>登录</h1>", unsafe_allow_html=True)
        email = st.text_input("邮箱", key="email")
        password = st.text_input("密码", type="password", key="password")
        if st.button("登录"):
            try:
                # 使用 Supabase 进行认证
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
        st.markdown("</div>", unsafe_allow_html=True)

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
