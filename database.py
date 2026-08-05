import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool


def get_connection():
    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=os.environ["PGPORT"],
        database=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        sslmode=os.environ["PGSSLMODE"],
    )


engine = create_engine(
    "postgresql+psycopg2://",
    creator=get_connection,
    poolclass=NullPool,
)
