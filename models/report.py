from decimal import Decimal

from pydantic import BaseModel


class Report(BaseModel):
    """
    A model to encapsulate a net-income report. Good for a JSON response.
    """

    gross_revenue: Decimal
    expenses: Decimal
    net_revenue: Decimal
