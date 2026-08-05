import os
from sqlalchemy import create_engine
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

database = w.apps.get_app_database(
    app_name=os.environ["DATABRICKS_APP_NAME"],
    resource_key="database"
)

engine = create_engine(database.connection_string)
