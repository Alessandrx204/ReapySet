import streamlit as st


st.title("Dashboard")

st.write("A simple starting point for your dashboard.")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Users",
        value="1,024",
        delta="12%",
    )

with col2:
    st.metric(
        label="Sessions",
        value="2,350",
        delta="8%",
    )

with col3:
    st.metric(
        label="Conversion",
        value="4.2%",
        delta="-0.3%",
    )

st.divider()

value = st.slider(
    "Example value",
    min_value=0,
    max_value=100,
    value=50,
)

st.progress(value / 100)

st.caption(f"Current value: {value}%")