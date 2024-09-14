import streamlit as st

# 初始化 session_state 变量
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def main():
    if not st.session_state["logged_in"]:
        st.warning("请先登录。")
        # 跳转回登录页面
        st.experimental_set_query_params(page="login")
        st.stop()

    st.title("仪表板")
    st.write("欢迎来到仪表板页面。")

    # 添加登出按钮
    if st.button("退出登录"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.success("已成功退出登录")
        # 跳转回登录页面
        st.experimental_set_query_params(page="login")
        st.experimental_rerun()

if __name__ == "__main__":
    main()
