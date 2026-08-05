import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import engine

st.title("Support Ticket System")

with engine.connect() as conn:
    tickets = pd.read_sql(
        text("SELECT * FROM tickets"),
        conn
    )

st.dataframe(tickets)
