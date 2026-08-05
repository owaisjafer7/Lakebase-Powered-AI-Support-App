import os
from sqlalchemy import create_engine

if "database" not in os.environ:
    raise Exception("database resource is not available")

DATABASE_URL = os.environ["database"]

engine = create_engine(DATABASE_URL)
