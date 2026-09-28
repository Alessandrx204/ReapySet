import streamlit as st


st.set_page_config(
    page_title="Streamlit App",
    page_icon="🚀",
    layout="wide",
)

st.title("Streamlit App")
st.caption("A Streamlit application generated with ReapySet.")

st.write(
    """
    Welcome to your Streamlit project.

    Use the sidebar to navigate between pages or start building
    your application here.
    """
)

st.subheader("Get started")

name = st.text_input(
    "Your name",
    placeholder="Enter your name",
)

if st.button("Continue", type="primary"):
    if name:
        st.success(f"Welcome, {name}!")
    else:
        st.warning("Please enter your name.")