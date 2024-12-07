import datetime
from decimal import Decimal
from enum import Enum

from sqlmodel import Field, SQLModel
from ksuid import Ksuid


class IncomeOrExpense(str, Enum):
    income = "Income"
    expense = "Expense"


class Transaction(SQLModel, table=True):
    """
    The model used for the database - as declared by table=True.

    None of the fields are suitable to mark as Index fields - but Field does
    support notation to make it Indexable.
    """

    # Chosen to use KSUID type for id field so they can be constructed before
    # they reach the database. And so the database can hold two transactions that
    # otherwise would be the same.
    id: str = Field(default=Ksuid(), primary_key=True)
    date: datetime.date
    category: IncomeOrExpense
    amount: Decimal
    memo: str
