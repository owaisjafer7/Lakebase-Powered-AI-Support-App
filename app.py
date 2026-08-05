import streamlit as st
import pandas as pd
from database import engine
from sqlalchemy import text

st.set_page_config(page_title="Support Ticket System")

st.title("🎫 Support Ticket System")
st.success("Connected to Lakebase PostgreSQL")

# Create table if it does not exist
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS tickets (
            id SERIAL PRIMARY KEY,
            customer VARCHAR(100),
            title VARCHAR(255),
            description TEXT,
            status VARCHAR(50),
            priority VARCHAR(50)
        )
    """))

# Add sample ticket once
with engine.begin() as conn:
    count = conn.execute(text("SELECT COUNT(*) FROM tickets")).scalar()

    if count == 0:
        conn.execute(text("""
            INSERT INTO tickets 
            (customer, title, description, status, priority)
            VALUES
            ('Alice', 'Cannot login', 'Password reset not working', 'Open', 'High'),
            ('Bob', 'Billing issue', 'Wrong invoice amount', 'In Progress', 'Medium'),
            ('Charlie', 'Feature request', 'Requesting dark mode', 'Closed', 'Low')
        """))


st.subheader("Tickets")

with engine.connect() as conn:
    df = pd.read_sql(
        "SELECT * FROM tickets",
        conn
    )

st.dataframe(df, use_container_width=True)


st.subheader("Create New Ticket")

customer = st.text_input("Customer")
title = st.text_input("Issue Title")
description = st.text_area("Description")
priority = st.selectbox(
    "Priority",
    ["Low", "Medium", "High"]
)

if st.button("Submit Ticket"):

    with engine.begin() as conn:
        conn.execute(
            text("""
            INSERT INTO tickets
            (customer, title, description, status, priority)
            VALUES
            (:customer, :title, :description, 'Open', :priority)
            """),
            {
                "customer": customer,
                "title": title,
                "description": description,
                "priority": priority
            }
        )

    st.success("Ticket created!")
    st.rerun()
