import os
import streamlit as st

st.title("Environment Check")

for key in sorted(os.environ.keys()):
    if "PG" in key or "DB" in key or "DATABASE" in key:
        st.write(key)

raise Exception("stop")
