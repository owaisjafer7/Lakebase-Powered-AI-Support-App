import os
from sqlalchemy import create_engine

DATABASE_URL = (
    f"postgresql://{os.environ['PGUSER']}@"
    f"{os.environ['PGHOST']}:"
    f"{os.environ['PGPORT']}/"
    f"{os.environ['PGDATABASE']}?sslmode=require"
)

engine = create_engine(DATABASE_URL)
