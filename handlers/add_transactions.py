from fastapi import HTTPException
from sqlmodel import Session
from models.transaction import (
    TransactionCreate,
    TransactionPublic,
)
from storage.sqldb import store_transactions

#  TODO should become redundant
# from storage.in_memory_store import store_transactions


def add_transactions(csv_data: bytes, session: Session) -> list[TransactionPublic]:
    """
    Return type is the <Public> variant of a Transaction - suitable for a JSON response.
    """
    created_transactions = build_transactions(csv_data)
    transactions_for_response = store_transactions(created_transactions, session)
    return transactions_for_response


def build_transactions(csv_data: bytes) -> list[TransactionCreate]:
    """
    Return type is the <Create> variant of a Transaction - suitable for
    constructing one from JSON input.
    """
    try:
        s = csv_data.decode("UTF-8")
    except Exception as err:
        raise HTTPException(
            status_code=400, detail=f"Cannot decode your CSV input. Details: {str(err)}"
        )

    lines = s.splitlines()

    transactions: list[TransactionCreate] = []
    for line in lines:
        if len(line) == 0:
            continue
        if line.isspace():
            continue
        if line[0] == "#":
            continue

        transaction = parse_transaction(line)
        transactions.append(transaction)

    return transactions


def parse_transaction(line: str) -> TransactionCreate:
    """
    Return type is the <Create> variant of a Transaction - suitable for
    constructing one from JSON input.
    """
    fields = [field.strip() for field in line.split(",")]
    n_fields = len(fields)
    if n_fields != 4:
        raise HTTPException(
            status_code=400, detail=f"Should be 4 fields, not {n_fields} ({line})"
        )
    try:
        # We suppress type hint warnings because we are relying on Pydantic model-wide validation of these string inputs.
        transaction = TransactionCreate(
            date=fields[0],  # type: ignore
            category=fields[1],  # type: ignore
            amount=fields[2],  # type: ignore
            memo=fields[3],  # type: ignore
        )
    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot parse one of the CSV lines. Details: {str(err)}",
        )
    return transaction
