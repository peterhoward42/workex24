"""
We create some module-scope, singleton artefacts to provide global access to the database.
"""

from typing import Annotated
from sqlmodel import create_engine, Session
from fastapi import Depends

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


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
