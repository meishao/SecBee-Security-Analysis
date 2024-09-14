import streamlit as st

def logout_page(supabase):
    st.title("退出登录")
    st.write("正在退出...")
    if st.button("退出"):
        # 使用 Supabase 进行登出
        supabase.auth.sign_out()
        st.session_state.clear()
        st.rerun()

