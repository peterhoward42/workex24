from fastapi import HTTPException
from models.transaction import TransactionDBModel, TransactionRequestModel
from sqlmodel import SQLModel, Session
from sqlalchemy import delete, select


"""
This module isolates the database crud operations to a single place.

Note the functions in this module DO NOT COMMIT the database changes.
Because the commit properly belongs at a higher
where the context-managed session lifecycle is managed.
"""


def clear(session: Session) -> int:
    """
    Removes all TransactionDBModel rows.
    """
    statement = select(TransactionDBModel)
    transactions = session.scalars(statement).all()
    for t in transactions:
        session.delete(t)
    return len(transactions)


def store_transactions(
    transactions: list[TransactionRequestModel], session: Session
) -> list[TransactionDBModel]:
    """
    Replaces any transactions in the database with the given transactions.
    """

    # Remove existing rows (the declared contract).
    clear(session)

    db_transactions: list[TransactionDBModel] = []
    for t in transactions:
        db_transaction = TransactionDBModel.model_validate(t)
        db_transactions.append(db_transaction)
    session.add_all(db_transactions)
    # We don't do a session.refresh() because we already have a fully populated datamodel.
    return db_transactions


def retrieve_transactions(session: Session) -> list[TransactionDBModel]:
    """
    Fetches a list of all transactions from the database.
    """
    statement = select(TransactionDBModel)
    transactions = session.scalars(statement).all()

    # Ignoring mypy warning because all() returns an internal Sequence type, but
    # want to return a plain list from this function.
    return transactions  # type: ignore
