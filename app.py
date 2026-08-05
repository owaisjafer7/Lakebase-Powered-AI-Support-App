import streamlit as st
import pandas as pd
from sqlalchemy import text
from lakebase import engine


st.set_page_config(
    page_title="Support Ticket System",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>

    .main {
        background: linear-gradient(135deg,#667eea,#764ba2);
        padding: 2rem;
    }

    .stApp > div:first-child {
        background:white;
        border-radius:20px;
        padding:2rem;
    }

    h1 {
        color:#1a202c;
        text-align:center;
    }

    .stButton > button {
        background:linear-gradient(135deg,#667eea,#764ba2);
        color:white;
        border-radius:8px;
        font-weight:600;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    "<h1>🎫 Support Ticket System</h1>",
    unsafe_allow_html=True
)

try:

    with engine.connect() as conn:

        tickets = pd.read_sql(
            """
            SELECT *
            FROM tickets
            ORDER BY ticket_id
            """,
            conn
        )

except Exception as e:

    st.error("Could not load tickets")
    st.exception(e)
    st.stop()


st.subheader("📊 Dashboard Overview")


total = len(tickets)

open_count = len(
    tickets[tickets["ticket_status"] == "Open"]
)

progress_count = len(
    tickets[tickets["ticket_status"] == "In Progress"]
)

resolved_count = len(
    tickets[tickets["ticket_status"] == "Resolved"]
)


c1,c2,c3,c4 = st.columns(4)


with c1:
    st.metric("Total Tickets", total)

with c2:
    st.metric("Open", open_count)

with c3:
    st.metric("In Progress", progress_count)

with c4:
    st.metric("Resolved", resolved_count)


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📋 Tickets",
        "➕ Create Ticket",
        "💬 Messages",
        "⚙️ Update Status"
    ]
)

with tab1:

    st.subheader("📋 All Support Tickets")

    filter_status = st.selectbox(
    "Filter by Status",
    [
        "All",
        "Open",
        "In Progress",
        "Resolved"
    ],
    key="ticket_filter"
)


if filter_status != "All":

    filtered_tickets = tickets[
        tickets["ticket_status"] == filter_status
    ]

else:

    filtered_tickets = tickets


st.dataframe(
    filtered_tickets,
    use_container_width=True,
    hide_index=True
)

with tab2:

    st.subheader("➕ Create New Ticket")


    with st.form(
        "create_ticket_form",
        clear_on_submit=True
    ):

        title = st.text_input(
            "Ticket Title"
        )

        created_by = st.text_input(
            "Created By"
        )


        status = st.selectbox(
            "Status",
            [
                "Open",
                "In Progress",
                "Resolved"
            ],
            key="create_ticket_status"
        )

        priority = st.selectbox(
    "Priority",
    [
        "Low",
        "Medium",
        "High",
        "Critical"
    ],
    key="ticket_priority"
)


        submit = st.form_submit_button(
            "Create Ticket"
        )


        if submit:

            if not title or not created_by:

                st.warning(
                    "Please fill all fields."
                )

            else:

                with engine.begin() as conn:

                    result = conn.execute(
                        text(
                            """
                            INSERT INTO tickets
                            (
                                ticket_title,
                                ticket_status,
                                ticket_created_by,
                                ticket_priority
                            )
                            VALUES
                            (
                                :title,
                                :status,
                                :creator,
                                :priority
                            )

                            RETURNING ticket_id
                            """
                        ),
                        {
                            "title":title,
                            "status":status,
                            "creator":created_by,
                            "priority": priority
                        }
                    )


                    new_ticket_id = result.scalar()



                    conn.execute(
                        text(
                            """
                            INSERT INTO ticket_messages
                            (
                                ticket_id,
                                ticket_message_text,
                                ticket_author
                            )

                            VALUES
                            (
                                :id,
                                :message,
                                :author
                            )
                            """
                        ),
                        {
                            "id":new_ticket_id,
                            "message":"Ticket created.",
                            "author":created_by
                        }
                    )


                st.success(
                    f"Ticket #{new_ticket_id} created!"
                )

                st.rerun()

with tab3:

    st.subheader("💬 Ticket Messages")


    with st.expander(
        "🔍 View Messages",
        expanded=True
    ):


        view_id = st.number_input(
            "Ticket ID",
            min_value=1,
            step=1,
            key="view_ticket_id"
        )


        if st.button(
            "View Messages",
            key="view_messages_button"
        ):


            with engine.connect() as conn:


                ticket = pd.read_sql(
                    text(
                        """
                        SELECT *
                        FROM tickets
                        WHERE ticket_id=:id
                        """
                    ),
                    conn,
                    params={
                        "id":view_id
                    }
                )


                messages = pd.read_sql(
                    text(
                        """
                        SELECT
                            ticket_message_id,
                            ticket_message_text,
                            ticket_author,
                            ticket_created_at

                        FROM ticket_messages

                        WHERE ticket_id=:id

                        ORDER BY ticket_message_id
                        """
                    ),
                    conn,
                    params={
                        "id":view_id
                    }
                )


            if ticket.empty:

                st.warning(
                    "Ticket not found."
                )

            else:

                st.info(
                    f"""
                    Ticket:
                    {ticket.iloc[0]['ticket_title']}

                    Status:
                    {ticket.iloc[0]['ticket_status']}
                    """
                )


                if messages.empty:

                    st.info(
                        "No messages yet."
                    )

                else:

                    st.dataframe(
                        messages,
                        use_container_width=True,
                        hide_index=True
                    )



    st.divider()


    with st.expander(
        "➕ Add Message"
    ):


        with st.form(
            "add_message_form",
            clear_on_submit=True
        ):


            message_ticket_id = st.number_input(
                "Ticket ID",
                min_value=1,
                step=1,
                key="add_message_ticket_id"
            )


            message = st.text_area(
                "Message"
            )


            author = st.text_input(
                "Author"
            )


            submit_message = st.form_submit_button(
                "Add Message"
            )


            if submit_message:


                if not message or not author:

                    st.warning(
                        "Message and author required."
                    )


                else:

                    with engine.begin() as conn:

                        conn.execute(
                            text(
                                """
                                INSERT INTO ticket_messages
                                (
                                    ticket_id,
                                    ticket_message_text,
                                    ticket_author
                                )

                                VALUES
                                (
                                    :id,
                                    :message,
                                    :author
                                )
                                """
                            ),
                            {
                                "id":message_ticket_id,
                                "message":message,
                                "author":author
                            }
                        )


                    st.success(
                        "Message added!"
                    )

                    st.rerun()


with tab4:


    st.subheader(
        "⚙️ Update Ticket Status"
    )


    with st.form(
        "update_status_form"
    ):


        ticket_id = st.number_input(
            "Ticket ID",
            min_value=1,
            step=1,
            key="update_ticket_id"
        )


        new_status = st.selectbox(
            "New Status",
            [
                "Open",
                "In Progress",
                "Resolved"
            ],
            key="update_status_value"
        )


        update = st.form_submit_button(
            "Update Status"
        )


        if update:


            with engine.begin() as conn:

                conn.execute(
                    text(
                        """
                        UPDATE tickets

                        SET ticket_status=:status

                        WHERE ticket_id=:id
                        """
                    ),
                    {
                        "status":new_status,
                        "id":ticket_id
                    }
                )


            st.success(
                "Status updated!"
            )

            st.rerun()


st.divider()

st.markdown(
    """
    <center>
    🚀 Built with Streamlit + Lakebase PostgreSQL
    <br>
    Powered by Databricks Apps
    </center>
    """,
    unsafe_allow_html=True
)