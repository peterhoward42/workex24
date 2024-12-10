from fastapi import HTTPException
from sqlmodel import Session
from db.db_crud import retrieve_transactions
from models.transaction import TransactionDBModel, IncomeOrExpense
from models.report import Report
from decimal import Decimal


def report(session: Session) -> Report:
    transactions = retrieve_transactions(session)

    if len(transactions) == 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot generate report because there are no stored transactions - use the /transactions endpoint to put some in.",
        )

    gross_revenue = sum_transactions_of_type(transactions, IncomeOrExpense.income)
    expenses = sum_transactions_of_type(transactions, IncomeOrExpense.expense)

    net_revenue = gross_revenue - expenses

    # This try/except is primarily to reveal programming errors during development.
    try:
        report = Report(
            gross_revenue=gross_revenue, expenses=expenses, net_revenue=net_revenue
        )
    except Exception as err:
        raise HTTPException(
            500,
            f"Internal error: failed to parse stored transactions. Details: {str(err)}",
        )

    return report


def sum_transactions_of_type(
    all_transactions: list[TransactionDBModel], category: IncomeOrExpense
) -> Decimal:
    transactions = [t for t in all_transactions if t.category == category]
    amounts = [t.amount for t in transactions]
    return sum(amounts, Decimal(0))
