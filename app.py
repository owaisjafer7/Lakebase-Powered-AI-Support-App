import streamlit as st
from database import engine

st.title("Support Ticket System")

try:
    with engine.connect() as conn:
        st.success("Connected to Lakebase!")

except Exception as e:
    st.error("Could not connect to Lakebase")
    st.exception(e)
