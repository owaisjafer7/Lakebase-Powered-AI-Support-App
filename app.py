import streamlit as st
import pandas as pd
from database import engine


st.title("Support Ticket System")


st.header("All Tickets")


with engine.connect() as conn:
    tickets = pd.read_sql(
        "SELECT * FROM tickets ORDER BY created_at DESC",
        conn
    )


st.dataframe(tickets)