import os
from sqlalchemy import create_engine

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL is missing")

engine = create_engine(DATABASE_URL)
