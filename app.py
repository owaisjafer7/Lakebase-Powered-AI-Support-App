import streamlit as st
import pandas as pd
from sqlalchemy import text
from database import engine

st.set_page_config(page_title="Support Ticket System")

st.title("Lakebase-Powered AI Support Ticket App")

st.success("Connected to Lakebase PostgreSQL")

st.subheader("All Tickets")

with engine.connect() as conn:
    tickets = pd.read_sql("""SELECT * FROM tickets ORDER BY ticket_id""",conn)

st.dataframe(
    tickets,
    use_container_width=True
)

st.subheader("Create New Ticket")

ticket_title = st.text_input("Ticket Title")
created_by = st.text_input("Created By")

ticket_status = st.selectbox("Status", ["Open", "In Progress", "Resolved"], key="create_ticket_status"
)

if st.button("Create Ticket"):
    if ticket_title and created_by:
        with engine.begin() as conn:
            conn.execute(text(
                """INSERT INTO tickets
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
                """),
                {
                    "title": ticket_title,
                    "status": ticket_status,
                    "created_by": created_by
                }
            )

        st.success("Ticket created successfully!")
        st.rerun()
    else:
        st.warning("Please enter a title and creator.")

st.subheader("View Ticket Messages")

view_ticket_id = st.number_input(
    "Ticket ID",
    min_value=1,
    step=1,
    key="view_messages_id"
)


if st.button("View Messages"):
    with engine.connect() as conn:
        messages = pd.read_sql(
            text("""
                SELECT *
                FROM ticket_messages
                WHERE ticket_id = :id
                ORDER BY ticket_message_id
            """),
            conn,
            params={
                "id": view_ticket_id
            }
        )

    if len(messages) > 0:
        st.dataframe(
            messages,
            use_container_width=True
        )
    else:
        st.info("No messages found for this ticket.")

st.subheader("Add Message")

message_ticket_id = st.number_input(
    "Ticket ID for Message",
    min_value=1,
    step=1,
    key="add_message_id"
)

message_text = st.text_area(
    "Message"
)

message_author = st.text_input(
    "Author"
)


if st.button("Add Message"):

    if message_text and message_author:

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
                    "author": message_author
                }
            )

        st.success("Message added successfully!")
        st.rerun()

    else:
        st.warning("Please enter message and author.")


st.subheader("Update Ticket Status")

update_ticket_id = st.number_input(
    "Ticket ID to Update",
    min_value=1,
    step=1,
    key="update_status_id"
)

new_status = st.selectbox(
    "New Status",
    [
        "Open",
        "In progress",
        "Resolved"
    ],
    key="update_status_select"
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

    st.success("Ticket status updated!")
    st.rerun()
