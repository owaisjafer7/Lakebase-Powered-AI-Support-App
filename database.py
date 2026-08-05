import os
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

def get_connection():
    import psycopg2

    return psycopg2.connect(
        host=os.environ["PGHOST"],
        port=os.environ["PGPORT"],
        database=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        sslmode="require"
    )

engine = create_engine(
    "postgresql+psycopg2://",
    creator=get_connection,
    poolclass=NullPool
)
