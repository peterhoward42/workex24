import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel

class IncomeOrExpense(str, Enum):
    income = 'Income'
    expense = 'Expense'

class Transaction(BaseModel):
    date: datetime.date
    category: IncomeOrExpense 
    amount: Decimal
    memo: str