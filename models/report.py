from decimal import Decimal

from pydantic import BaseModel


class Report(BaseModel):
    gross_revenue: Decimal
    expenses: Decimal
    net_revenue: Decimal
