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
    # 使用 CSS 美化登录页面
    st.markdown(
        """
        <style>
        .login-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            padding: 0;
        }
        .login-container img {
            width: 200px;
            margin-bottom: 20px;
        }
        .login-container h1 {
            margin-bottom: 30px;
        }
        /* 调整输入框样式 */
        div[data-baseweb="input"] {
            width: 300px !important;
            margin-bottom: 20px !important;
        }
        div[data-baseweb="input"] > div {
            width: 100% !important;
        }
        div[data-baseweb="input"] > div > input {
            padding: 10px !important;
            border: 1px solid #ccc !important;
            border-radius: 5px !important;
        }
        /* 调整按钮样式 */
        div.stButton > button {
            width: 320px !important;
            height: 45px !important;
            background-color: #4CAF50 !important;
            color: white !important;
            border: none !important;
            border-radius: 5px !important;
            cursor: pointer !important;
        }
        div.stButton > button:hover {
            background-color: #45a049 !important;
        }
        /* 消除 Streamlit 默认的顶部间距 */
        div.block-container {
            padding-top: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 创建登录容器
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # 添加 Logo
    st.image('logo.png')  # 可以指定 width 参数，例如 width=200

    # 登录标题
    st.markdown('<h1>登录</h1>', unsafe_allow_html=True)

    # 邮箱和密码输入框
    email = st.text_input("邮箱", key="email")
    password = st.text_input("密码", type="password", key="password")

    # 登录按钮
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

    # 结束登录容器
    st.markdown('</div>', unsafe_allow_html=True)

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
