from sqlalchemy import create_engine
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.apps import App

client = WorkspaceClient()

database_credential = client.apps.get_database_credential(
    app_name="ticketing-system-app"
)

DATABASE_URL = (
    f"postgresql://{database_credential.username}:"
    f"{database_credential.password}@"
    f"{database_credential.host}:"
    f"{database_credential.port}/"
    f"{database_credential.database}"
    "?sslmode=require"
)

engine = create_engine(DATABASE_URL)
