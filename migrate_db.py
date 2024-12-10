from db.db_config import engine
from sqlmodel import SQLModel

"""
This module provides a main function that will create or migrate the
database.

It is NOT called on API startup so that it can be treated as a separate
process in a horizontally scaled context.
"""

"""
This <import *> is necessary for its side effects.

It populates the SQLModel.metadata.tables class variable so the create_all() method
knows about the tables it should detect.
"""
from models.transaction import *

if __name__ == "__main__":
    meta = SQLModel.metadata
    SQLModel.metadata.create_all(bind=engine)
