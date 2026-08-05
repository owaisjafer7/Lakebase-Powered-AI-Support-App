import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import engine


st.title("Support Ticket System")


try:
    with engine.connect() as conn:
        df = pd.read_sql(
            text("SELECT * FROM tickets LIMIT 10"),
            conn
        )

    st.success("Connected to Lakebase!")
    st.dataframe(df)

except Exception as e:
    st.error("Could not connect to Lakebase")
    st.exception(e)
