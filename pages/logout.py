import streamlit as st

def logout_page(supabase):
    st.title("退出登录")
    if st.button("退出"):
        # 使用 Supabase 进行登出
        supabase.client.auth.sign_out()
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.success("已成功退出登录")
        # 重定向到登录页面
        st.query_params["page="] = "login"
        st.rerun()
