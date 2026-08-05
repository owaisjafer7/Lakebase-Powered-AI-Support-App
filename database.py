import os
from sqlalchemy import create_engine

DATABASE_URL = os.environ["LAKEBASE_URL"]

engine = create_engine(DATABASE_URL)
