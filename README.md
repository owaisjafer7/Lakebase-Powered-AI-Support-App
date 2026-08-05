Lakebase-Powered AI Support App Documentation
Project Overview

This project is an internal support ticket management application built using Databricks Apps, Streamlit, and Lakebase PostgreSQL.

The application allows support users to:

View existing support tickets
Create new tickets
View messages associated with tickets
Add messages to tickets
Update ticket status
Track ticket statistics

All application data is stored and retrieved from Lakebase. No ticket information is hard-coded into the application.

Architecture Overview

The application contains three main components:

1. Streamlit Application (app.py)

The user interface is built using Streamlit.

Responsibilities:

Display tickets
Collect user input
Submit database changes
Display ticket messages
Show ticket statistics

The app communicates with Lakebase through SQL queries using SQLAlchemy and psycopg2.

2. Database Connection (database.py)

The database connection layer handles communication between the Streamlit application and Lakebase PostgreSQL.

Responsibilities:

Create the database engine
Authenticate securely
Provide connections for queries

Database credentials are not stored in the source code.

3. Lakebase PostgreSQL Database

Lakebase stores the operational data for the application.

The database contains two related tables:

tickets

Stores the main ticket information.

Columns:

Column	Description
ticket_id	Unique ticket identifier
ticket_title	Ticket subject
ticket_status	Current ticket status
ticket_created_by	Person who created the ticket
ticket_created_at	Creation timestamp
ticket_priority	Ticket importance level
ticket_messages

Stores conversations attached to tickets.

Columns:

Column	Description
ticket_message_id	Unique message identifier
ticket_id	Related ticket
ticket_message_text	Message content
ticket_author	Person who wrote message
ticket_created_at	Message timestamp

Relationship:

tickets.ticket_id
        |
        |
ticket_messages.ticket_id

A single ticket can contain multiple messages.

Database Design

The database was designed around a one-to-many relationship.

Example:

Ticket:

Ticket #1
Login failed
Status: Open
Created by: Owais

Messages:

Message 1:
"I cannot log into my account."

Message 2:
"We are looking into the issue."

This design allows multiple support conversations to belong to one ticket.

Features Implemented
Ticket Management

Users can:

✅ View all tickets
✅ Create new tickets
✅ Update ticket status
✅ Assign ticket priority

Message Management

Users can:

✅ View messages for a selected ticket
✅ Add new messages
✅ Track message authors and timestamps

Dashboard Statistics

The application displays:

Total ticket count
Open tickets
In-progress tickets
Resolved tickets

These values are calculated dynamically from Lakebase.

Deployment Process

Steps completed:

Created Lakebase database project
Created PostgreSQL schema
Added sample ticket data
Created Databricks App
Connected application to Lakebase
Deployed Streamlit application
Tested database operations
Problems Encountered and Solutions
Database Authentication
Problem:

The application initially failed with:

fe_sendauth: no password supplied
Cause:

The app was reaching Lakebase but did not have valid database authentication.

Solution:

Configured the correct Lakebase password authentication and database connection settings.

Incorrect Table Columns
Problem:

The app attempted to query:

SELECT * FROM tickets ORDER BY id

but the database used:

ticket_id
Solution:

Updated application SQL queries to match the Lakebase schema.

Duplicate Streamlit Widgets
Problem:

Streamlit generated:

DuplicateWidgetID
Cause:

Multiple input widgets had identical structures.

Solution:

Added unique widget keys:

Example:

key="view_ticket_messages_id"
Security Considerations

The application does not include:

Database passwords
API keys
Secret values

Credentials are handled through the Databricks environment instead of being stored in source code.

Reflection

The most difficult part of this project was configuring the connection between Databricks Apps and Lakebase and troubleshooting authentication issues. Lakebase differs from traditional analytics tables because it is designed for operational applications where data is continuously created, updated, and retrieved in real time. The project showed how an application can use a relational database backend to support workflows instead of only analyzing historical data. The next feature I would add is an AI support assistant that summarizes tickets and recommends responses.

Optional: Add an "AI Assistance" note

If you are worried about using AI, I would not hide it. A professional way to describe it:

AI tools were used as development assistance for debugging, code organization, and documentation. All application features were tested, configured, and validated against the Lakebase environment.

That is a normal engineering workflow now.
