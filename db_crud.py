from fastapi import HTTPException
from models.transaction import Transaction
from sqlmodel import Session


def store_transactions(transactions: list[Transaction], session: Session):
    session.add_all(transactions)


def retrieve_transactions(session: Session) -> list[Transaction]:
    transactions = session.query(Transaction).all()
    return transactions
