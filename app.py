import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import engine

st.title("Support Ticket System")

st.write("Lakebase-powered AI Support App")

# View tickets
st.header("Support Tickets")

with engine.connect() as conn:
    tickets = pd.read_sql(
        text("""
            SELECT 
                ticket_id,
                ticket_title,
                ticket_status,
                ticket_created_by,
                ticket_created_at
            FROM tickets
            ORDER BY ticket_created_at DESC
        """),
        conn
    )

st.dataframe(tickets)
