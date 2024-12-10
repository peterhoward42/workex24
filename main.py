from typing import Annotated
from fastapi import FastAPI, File
import uvicorn

from handlers import make_report
from handlers.add_transactions import parse_and_store_transactions
from models.report import Report
from models.transaction import TransactionRequestModel, TransactionDBModel
from db.db_config import SessionDep

"""
This is the entry point module for the FastAPI API implementation.

It is primarily a router, intended to be deployed inside an external
server. (See if __name__ == "__main__":) below.
"""


description = """
Tax Accounts API helps you generate a tax submission. 🚀

You can:

* **Upload transactions from a CSV file**
* **Then get a summary net-revenue report**
"""

app = FastAPI(title="Tax Accounts API", description=description)


@app.post(
    "/transactions",
    response_model=list[TransactionDBModel],
    status_code=201,
    name="Upload transactions from CSV file",
)
def handle_transactions(
    data: Annotated[bytes, File()], session: SessionDep
) -> list[TransactionDBModel]:
    """
    The file you choose for '''data''' in the request body should contain lines like
    these:

    ```
    2020-07-01, Expense, 18.77, Fuel
    2020-07-04, Income, 40.00, 347 Woodrow
    ```
    """
    transactions = parse_and_store_transactions(data, session)

    # We only commit the changes to the database if no exceptions have
    # been raised during the loading of the CSV data.
    session.commit()
    return transactions


@app.get("/report", name="Get a summary report")
def handle_get_report(session: SessionDep) -> Report:
    return make_report.report(session)
    # No Db commit here - because it is purely a reading operation.


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
