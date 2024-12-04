import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class IncomeOrExpense(str, Enum):
    income = "Income"
    expense = "Expense"


class Transaction(BaseModel):
    """The model used to encapsulate a single transaction for both incoming requests and storage."""

    date: datetime.date
    category: IncomeOrExpense
    amount: Decimal
    memo: str
