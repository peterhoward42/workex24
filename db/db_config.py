"""
We create some module-scope, singleton artefacts to provide global access to the database.
"""

from typing import Annotated
from sqlmodel import create_engine, Session
from fastapi import Depends
import os

# Take the URL for the database connection from an environment variable
# when it is present, otherwise set it to a local SQLite file-based database.
#
# The default is useful for testing and during development.
url_from_env = os.environ.get("DATABASE_URL")
sql_url = url_from_env if url_from_env else "sqlite:///database.db"

connect_args = {"check_same_thread": False}

# We do not catch exceptions thrown by create_engine() delibarately. As this is
# a boot-time error arsing from a deployment mis-configuration, and the details are
# are useful.
engine = create_engine(sql_url, connect_args=connect_args)


def get_session():
    """
    get_session() is a python generator that only ever yields once!
    It yields a Session.

    The reason the yield is placed inside the with-as context manager,
    is so the __exit__ method of the context manager is not triggered
    at the time the yield is done - which it WOULD be if a return was used.
    I.e. the session continues to live while the context manager is
    paused.

    We can presume that the Session's __exit__ method returns the underlying
    connection to the connect pool.

    FastAPI obtains a session for each incoming request and disposes of it when that
    request has completed.
    """
    with Session(engine, expire_on_commit=False) as session:
        yield session


"""
This is just a bit of FastAPI DRY type hinting syntax for dependency injection.
You can use it like this on an endpoint handler to obtain a new Session
for each request handler.

def some_handler(..., session: SessionDep):
"""
SessionDep = Annotated[Session, Depends(get_session)]
