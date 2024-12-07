from db_config import engine
from sqlmodel import SQLModel

"""
This import is for its side effect.
It populates the SQLModel.metadata.tables class variable so the create_all() method
knows about the tables it should detect.
"""
from models.transaction import *

if __name__ == "__main__":
    meta = SQLModel.metadata
    SQLModel.metadata.create_all(bind=engine)
