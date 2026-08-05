import os
from sqlalchemy import create_engine

host = os.environ["PGHOST"]
port = os.environ["PGPORT"]
database = os.environ["PGDATABASE"]
user = os.environ["PGUSER"]


with open("/var/run/secrets/lakebase/password", "r") as f:
    password = f.read().strip()

DATABASE_URL = (
    f"postgresql://{user}:{password}@"
    f"{host}:{port}/{database}?sslmode=require"
)

engine = create_engine(DATABASE_URL)
