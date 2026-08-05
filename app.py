from databricks.sdk import WorkspaceClient
from sqlalchemy import create_engine
import os

w = WorkspaceClient()

connection = w.database.get_database_credential(
    database_instance_name="databricks_postgres"
)

DATABASE_URL = (
    f"postgresql://{connection.username}:"
    f"{connection.password}@"
    f"{os.environ['PGHOST']}:"
    f"{os.environ['PGPORT']}/"
    f"{os.environ['PGDATABASE']}"
)

engine = create_engine(DATABASE_URL)
