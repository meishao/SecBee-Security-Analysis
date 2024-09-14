import streamlit as st

# Verify the user's role
if not st.session_state.logged_in:
    st.warning("You do not have permission to view this page.")
    st.stop()

st.title("This page is available to super-admins")
st.markdown(f"You are currently logged with the role of {st.session_state}.")
