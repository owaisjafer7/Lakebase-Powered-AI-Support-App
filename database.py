from databricks_lakebase import Connection
from sqlalchemy import create_engine

connection = Connection()

engine = create_engine(
    "postgresql+psycopg2://",
    creator=connection.get_connection
)
