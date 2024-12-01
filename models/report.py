import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field

class Report(BaseModel):
    gross_revenue: Decimal
    expenses: Decimal 
    net_revenue: Decimal
