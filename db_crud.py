from fastapi import HTTPException
from models.transaction import TransactionDBModel, TransactionRequestModel
from sqlmodel import SQLModel, Session


def store_transactions(
    transactions: list[TransactionRequestModel], session: Session
) -> list[TransactionDBModel]:
    """
    If this works, collapse it to a generator.
    """
    db_transactions: list[TransactionDBModel] = []
    for t in transactions:
        db_transaction = TransactionDBModel.model_validate(t)
        db_transactions.append(db_transaction)
    session.add_all(db_transactions)
    # We don't do a session.refresh() because we already have fully populated datamodel.
    #
    # We don't do a session.commit() because the commit properly belongs in the top level request handler
    # where the context-managed session lifecycle is managed.
    return db_transactions


def retrieve_transactions(session: Session) -> list[TransactionDBModel]:
    transactions = session.query(TransactionDBModel).all()
    return transactions
