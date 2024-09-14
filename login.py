import streamlit as st
from st_supabase_connection import SupabaseConnection

@st.cache_resource
def init_supabase_connection():
    return SupabaseConnection(connection_name="supabase")

supabase = init_supabase_connection()

def main():
    # 如果已经登录，跳转到仪表板
    if st.session_state.get("logged_in"):
        st.experimental_set_query_params(page="dashboard")
        st.experimental_rerun()

    # 创建左右两列布局
    col1, col2 = st.columns([1, 1])

    with col1:
        # 检测当前主题
        theme = st.get_option("theme.base")
        if theme == "dark":
            image_path = "dark_mode_logo.png"  # 替换为暗色模式下的图片路径
        else:
            image_path = "light_mode_logo.png"  # 替换为亮色模式下的图片路径

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

                    # 登录成功后，跳转到仪表板
                    st.experimental_set_query_params(page="dashboard")
                    st.experimental_rerun()
                else:
                    st.error("登录失败，请检查您的邮箱和密码。")
            except Exception as e:
                st.error(f"登录时出错：{e}")
