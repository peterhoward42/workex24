from fastapi import HTTPException
from sqlmodel import Session

from db.db_crud import store_transactions
from models.transaction import TransactionDBModel, TransactionRequestModel


def parse_and_store_transactions(
    csv_data: bytes, session: Session
) -> list[TransactionDBModel]:
    """
    Parses the given CSV data, builds corresponding transactions, and stores them
    in the database.
    """
    transaction_requests = build_transactions(csv_data)
    db_transactions = store_transactions(transaction_requests, session)
    return db_transactions


def build_transactions(csv_data: bytes) -> list[TransactionRequestModel]:
    """
    Does the parse, and build part.
    """
    try:
        s = csv_data.decode("UTF-8")
    except Exception as err:
        raise HTTPException(
            status_code=400, detail=f"Cannot decode your CSV input. Details: {str(err)}"
        )

    lines = s.splitlines()

    transactions: list[TransactionRequestModel] = []
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


def parse_transaction(line: str) -> TransactionRequestModel:
    """
    Does the parse part.
    """
    fields = [field.strip() for field in line.split(",")]
    n_fields = len(fields)
    if n_fields != 4:
        raise HTTPException(
            status_code=400, detail=f"Should be 4 fields, not {n_fields} ({line})"
        )
    try:
        # The <fields> are strings. I.e. not the types declared in the TransactionRequestModel.
        # But the whole point of the TransactionRequestModel constructor is to perform type
        # convertion AND validation of the string inputs. That is why we disable mypy type checking for
        # them.
        transaction_request = TransactionRequestModel(
            date=fields[0],  # type: ignore
            category=fields[1],  # type: ignore
            amount=fields[2],  # type: ignore
            memo=fields[3],  # type: ignore
        )

    except Exception as err:
        raise HTTPException(
            status_code=400,
            detail=f"Hit a problem with one of the CSV lines. Details: {str(err)}",
        )
    return transaction_request
