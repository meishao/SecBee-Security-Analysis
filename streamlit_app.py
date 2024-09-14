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
    # 创建左右两列布局
    col1, col2 = st.columns([1, 1])  # 您可以调整比例，如 [1, 2]

    with col1:
        # 检测当前主题
        theme = st.get_option("theme.base")
        if theme == "dark":
            image_path = "dark_mode_image.png"  # 替换为暗色模式下的图片路径
        else:
            image_path = "light_mode_image.png"  # 替换为亮色模式下的图片路径

        # 使用 st.image 显示图片
        st.image(image_path, use_column_width=True)

    with col2:
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
                    # 设置查询参数并重定向到 dashboard
                    st.query_params["page"] = "dashboard"
                    st.rerun()
                else:
                    st.error("登录失败，请检查您的邮箱和密码。")
            except Exception as e:
                st.error(f"登录时出错：{e}")

# 获取当前的查询参数
query_params = st.query_params
page = query_params.get("page", "login")

if st.session_state.get("logged_in") and page == "dashboard":
    # 已登录且页面为 dashboard，加载 dashboard.py
    import dashboard
elif page == "login":
    login()
else:
    # 未知页面，重定向到登录页面
    st.query_params["page"] = "login"
    st.rerun()
