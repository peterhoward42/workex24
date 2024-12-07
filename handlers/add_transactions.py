from fastapi import HTTPException
from sqlmodel import Session

from db_crud import store_transactions
from models.transaction import Transaction


def parse_and_store_transactions(
    csv_data: bytes, session: Session
) -> list[Transaction]:
    """
    Return type is the <Public> variant of a Transaction - suitable for a JSON response.
    """
    transactions = build_transactions(csv_data)
    store_transactions(transactions, session)
    return transactions


def build_transactions(csv_data: bytes) -> list[Transaction]:
    try:
        s = csv_data.decode("UTF-8")
    except Exception as err:
        raise HTTPException(
            status_code=400, detail=f"Cannot decode your CSV input. Details: {str(err)}"
        )

    lines = s.splitlines()

    transactions: list[Transaction] = []
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


def parse_transaction(line: str) -> Transaction:
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
        transaction = Transaction(
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
