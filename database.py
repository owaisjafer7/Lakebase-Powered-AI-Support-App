import os
from sqlalchemy import create_engine

DATABASE_URL = os.environ["lakebase-url"]

engine = create_engine(DATABASE_URL)
