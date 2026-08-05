import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import engine

st.title("🎫 Support Ticket System")

st.write("Loading tickets from Lakebase...")

try:
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
                ORDER BY ticket_id
            """),
            conn
        )

    st.subheader("All Tickets")
    st.dataframe(tickets)

except Exception as e:
    st.error("Could not load tickets")
    st.write(e)
