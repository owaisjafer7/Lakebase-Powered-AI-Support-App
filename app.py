import os
from sqlalchemy import create_engine

DATABASE_URL = os.environ["database"]

engine = create_engine(DATABASE_URL)
