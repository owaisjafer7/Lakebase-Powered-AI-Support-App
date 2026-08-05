import os
from sqlalchemy import create_engine
from databricks.sdk import WorkspaceClient


client = WorkspaceClient()

credential = client.database.generate_database_credential(
    request_id=os.environ["DATABRICKS_APP_NAME"]
)

DATABASE_URL = (
    f"postgresql://"
    f"{os.environ['PGUSER']}:"
    f"{credential.token}@"
    f"{os.environ['PGHOST']}:"
    f"{os.environ['PGPORT']}/"
    f"{os.environ['PGDATABASE']}"
    "?sslmode=require"
)

engine = create_engine(DATABASE_URL)
