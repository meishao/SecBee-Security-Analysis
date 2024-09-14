import streamlit as st

def main():
    st.title("退出登录")
    if st.button("退出"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.success("已成功退出登录")

        # 跳转回登录页面
        st.experimental_set_query_params(page="login")
        st.experimental_rerun()
