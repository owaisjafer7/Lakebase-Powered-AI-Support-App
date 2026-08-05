import base64
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from databricks.sdk import WorkspaceClient


client = WorkspaceClient()


def get_secret(key):
    value = client.secrets.get_secret(
        "lakebase",
        key
    ).value

    return base64.b64decode(value).decode()


HOST = get_secret("host")
PORT = int(get_secret("port"))
DATABASE = get_secret("database")
USERNAME = get_secret("username")
PASSWORD = get_secret("password")


def get_connection():

    return psycopg2.connect(
        host=HOST,
        port=PORT,
        database=DATABASE,
        user=USERNAME,
        password=PASSWORD,
        sslmode="require",
    )


engine = create_engine(
    "postgresql+psycopg2://",
    creator=get_connection,
    poolclass=NullPool
)
