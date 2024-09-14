import streamlit as st

'''
st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
'''

st.title("SecBee AI Security Analysis")
fp = st.text_input("Upload analysis file:")

if st.button("Start"):
    st.write("Analyzing...")
