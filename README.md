# Lakebase-Powered AI Support App

## Project Overview

This project is an internal support ticket management application built using **Databricks Apps**, **Streamlit**, and **Lakebase PostgreSQL**.

The application allows support users to:

* View existing support tickets
* Create new tickets
* View messages associated with tickets
* Add messages to existing tickets
* Update ticket status
* Track ticket statistics
* Assign ticket priority levels

All application data is stored and retrieved from Lakebase. The application does not use hard-coded ticket information.

---

# Application Architecture

The application consists of three main components:

## 1. Streamlit Application (`app.py`)

The user interface is built using Streamlit.

Responsibilities:

* Display tickets from Lakebase
* Collect user input
* Create new tickets
* Add ticket messages
* Update ticket statuses
* Display dashboard statistics

The application communicates with Lakebase PostgreSQL using SQLAlchemy and psycopg2.

---

## 2. Database Connection (`database.py`)

The database connection layer manages communication between the application and Lakebase.

Responsibilities:

* Create the database engine
* Authenticate securely
* Provide database connections
* Execute database operations

Database credentials are not stored directly in the source code.

---

## 3. Lakebase PostgreSQL Database

Lakebase stores the operational data used by the support application.

The database contains two related tables:

---

# Database Schema

## `tickets` Table

Stores the main support ticket information.

| Column              | Description                    |
| ------------------- | ------------------------------ |
| `ticket_id`         | Unique ticket identifier       |
| `ticket_title`      | Ticket subject/title           |
| `ticket_status`     | Current ticket status          |
| `ticket_created_by` | User who created the ticket    |
| `ticket_created_at` | Ticket creation timestamp      |
| `ticket_priority`   | Importance level of the ticket |

---

## `ticket_messages` Table

Stores messages associated with support tickets.

| Column                | Description                    |
| --------------------- | ------------------------------ |
| `ticket_message_id`   | Unique message identifier      |
| `ticket_id`           | Related ticket identifier      |
| `ticket_message_text` | Message content                |
| `ticket_author`       | Person who created the message |
| `ticket_created_at`   | Message creation timestamp     |

---

## Table Relationship

The database uses a one-to-many relationship:

```
tickets.ticket_id
        |
        |
ticket_messages.ticket_id
```

A single ticket can contain multiple messages.

Example:

```
Ticket #1
Title: Login failed
Status: Open

Messages:
- User: I cannot log into my account.
- Support: We are looking into the issue.
```

---

# Features Implemented

## Ticket Management

Users can:

* View all support tickets
* Create new tickets
* Update ticket status
* Assign ticket priority

---

## Message Management

Users can:

* View messages for a selected ticket
* Add new messages
* Track message authors
* Track message timestamps

---

## Dashboard Statistics

The application dynamically displays:

* Total tickets
* Open tickets
* In Progress tickets
* Resolved tickets

These values are calculated directly from Lakebase data.

---

# Deployment Process

The following steps were completed:

1. Created a Lakebase database project
2. Created the PostgreSQL schema
3. Added sample ticket records
4. Added sample ticket messages
5. Created the Databricks App
6. Connected the application to Lakebase
7. Deployed the Streamlit application
8. Tested database read/write operations

---

# Challenges and Solutions

## Lakebase Authentication

### Problem

The application initially failed with:

```
fe_sendauth: no password supplied
```

### Cause

The application could reach the database server but did not have valid authentication credentials.

### Solution

Configured the correct Lakebase authentication method and database connection settings.

---

## Database Column Mismatch

### Problem

The application attempted to query columns that did not exist:

```
SELECT * FROM tickets ORDER BY id
```

However, the database schema used:

```
ticket_id
```

### Solution

Updated application SQL queries to match the Lakebase schema.

---

## Streamlit Duplicate Widget Error

### Problem

Streamlit returned:

```
DuplicateWidgetID
```

### Cause

Multiple widgets had identical structures and automatically generated the same internal key.

### Solution

Added unique keys to Streamlit widgets.

Example:

```python
key="view_ticket_messages_id"
```

---

# Security Considerations

The application does not contain:

* Database passwords
* API keys
* Secret tokens
* Hard-coded credentials

Database access is handled through the Databricks environment configuration.

---

# Testing Completed

The application was tested to confirm:

✅ Existing tickets load from Lakebase
✅ New tickets can be created
✅ Messages can be added to tickets
✅ Ticket status can be updated
✅ Changes persist after refreshing the application

---

# Bonus Features Completed

The following bonus challenges were implemented:

✅ Ticket priority
✅ Ticket status filtering
✅ Input validation and error messages
✅ Ticket statistics dashboard
✅ Improved visual design

---

# Reflection

The most difficult part of this project was configuring the connection between Databricks Apps and Lakebase and troubleshooting authentication issues. Lakebase differs from traditional analytics tables because it is designed for operational applications where data is continuously created, updated, and retrieved in real time. This project demonstrated how a relational database can support application workflows instead of only storing analytical data. The next feature I would add is an AI support assistant that summarizes tickets and recommends responses for support agents.

---

# AI Development Assistance

AI tools were used as development assistance for debugging, code organization, and documentation. All application features were manually configured, tested, and validated against the Lakebase environment.
