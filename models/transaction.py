import datetime
from decimal import Decimal
from enum import Enum

from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4


class IncomeOrExpense(str, Enum):
    income = "Income"
    expense = "Expense"


class TransactionRequestModel(SQLModel):
    """
    The model used to capture input data.
    Note the absence of an <uuid> field.
    """

    date: datetime.date
    category: IncomeOrExpense
    amount: Decimal
    memo: str


class TransactionDBModel(TransactionRequestModel, table=True):
    """
    The model used for the database.
    Note the table=True parameter.
    """

    """
    Use UUID type for uuid field so they can be constructed
    at construction-time (before they reach the database).
    And to make it harder to create a spurious value (than an int).
    """
    id: UUID = Field(default_factory=uuid4, primary_key=True)
