import datetime
from decimal import Decimal
from enum import Enum

from sqlmodel import Field, SQLModel


class IncomeOrExpense(str, Enum):
    income = "Income"
    expense = "Expense"


class TransactionBase(SQLModel):
    """
    The DRY base class for a Transaction
    """

    date: datetime.date
    category: IncomeOrExpense
    amount: Decimal
    memo: str


class TransactionDB(TransactionBase, table=True):
    """
    The model used for the database - as declared by table=True.

    None of the fields are suitable to mark as Index fields - but Field does
    support notation to make it Indexable.
    """

    """
    The id field will be None until such time it has been added to
    the database
    """
    id: int | None = Field(default=None, primary_key=True)

    date: datetime.date
    category: IncomeOrExpense
    amount: Decimal
    memo: str


class TransactionPublic(TransactionBase):
    """
    The form of a Transaction returned by requests.


    """

    """
    Returned transactions
    a) Cannot have a null id
    b) Could omit the <secret_name> from TransactionCreate (if it had one).
    """
    id: int


class TransactionCreate(TransactionBase):
    """
    The model used to validate and encapsulate incoming JSON for a transaction.

    Currently unused, but keeping it to make its role clear.
    The role can include the presence of "secret" fields.
    """

    pass
