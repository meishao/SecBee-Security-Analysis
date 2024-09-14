# logout.py

import streamlit as st
from st_supabase_connection import SupabaseConnection

# 初始化 Supabase 连接
@st.cache_resource
def init_supabase_connection():
    return SupabaseConnection(connection_name="supabase")

supabase = init_supabase_connection()

def logout():
    st.title("退出登录")
    if st.button("退出"):
        # 使用 Supabase 客户端进行登出
        supabase.client.auth.sign_out()
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.success("已成功退出登录")
        # 重定向到登录页面
        st.query_params()
        st.rerun()

if st.session_state.get("logged_in"):
    logout()
else:
    # 未登录，重定向到登录页面
    st.warning("您尚未登录，请先登录。")
    st.query_params()
    st.rerun()
