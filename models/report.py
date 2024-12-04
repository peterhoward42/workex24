from decimal import Decimal

from pydantic import BaseModel


class Report(BaseModel):
    """
    The model used to encapsualte the returned net income calculation for an API response.
    """

    gross_revenue: Decimal
    expenses: Decimal
    net_revenue: Decimal
