import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import engine

st.set_page_config(page_title="Support Ticket System")

st.title("🎫 Support Ticket System")

st.success("Connected to Lakebase PostgreSQL")

# Show tickets
st.subheader("Tickets")

with engine.connect() as conn:
    tickets = pd.read_sql(
        """
        SELECT *
        FROM tickets
        ORDER BY ticket_id
        """,
        conn
    )

st.dataframe(tickets, use_container_width=True)


# Create ticket
st.subheader("Create New Ticket")

title = st.text_input("Ticket Title")
created_by = st.text_input("Created By")

status = st.selectbox(
    "Status",
    [
        "Open",
        "In progress",
        "Resolved"
    ]
)

if st.button("Create Ticket"):

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO tickets
                (
                    ticket_title,
                    ticket_status,
                    ticket_created_by
                )
                VALUES
                (
                    :title,
                    :status,
                    :created_by
                )
                """
            ),
            {
                "title": title,
                "status": status,
                "created_by": created_by
            }
        )

    st.success("Ticket created successfully!")
    st.rerun()


# Ticket messages
st.subheader("Ticket Messages")

ticket_id = st.number_input(
    "Ticket ID",
    min_value=1,
    step=1
)

if st.button("View Messages"):

    with engine.connect() as conn:
        messages = pd.read_sql(
            text(
                """
                SELECT *
                FROM ticket_messages
                WHERE ticket_id = :id
                ORDER BY ticket_message_id
                """
            ),
            conn,
            params={"id": ticket_id}
        )

    st.dataframe(messages, use_container_width=True)

st.subheader("Add Message")

message_ticket_id = st.number_input(
    "Ticket ID",
    min_value=1,
    step=1
)

message_text = st.text_area("Message")

author = st.text_input("Author")


if st.button("Add Message"):

    with engine.begin() as conn:
        conn.execute(
            text("""
            INSERT INTO ticket_messages
            (
                ticket_id,
                ticket_message_text,
                ticket_author
            )
            VALUES
            (
                :ticket_id,
                :message,
                :author
            )
            """),
            {
                "ticket_id": message_ticket_id,
                "message": message_text,
                "author": author
            }
        )

    st.success("Message added!")

st.subheader("Update Ticket Status")

update_ticket_id = st.number_input(
    "Ticket ID to update",
    min_value=1,
    step=1
)

new_status = st.selectbox(
    "New Status",
    [
        "Open",
        "In progress",
        "Resolved"
    ]
)


if st.button("Update Status"):

    with engine.begin() as conn:
        conn.execute(
            text("""
            UPDATE tickets
            SET ticket_status = :status
            WHERE ticket_id = :id
            """),
            {
                "status": new_status,
                "id": update_ticket_id
            }
        )

    st.success("Status updated!")
