from fastapi import FastAPI, File
import uvicorn
from typing import Annotated, List

from models.transaction import Transaction
from models.report import Report
from handlers.add_transactions import add_transactions
from handlers.make_report import make_report


description = """
Tax Accounts API helps you generate a tax submission. 🚀

You can:

* **Upload transactions from a CSV file**
* **Then get a summary net-revenue report**
"""
app = FastAPI(title="Tax Accounts API", description=description)

@app.post("/transactions", status_code=201, name='Upload transactions from CSV file')
def handle_transactions(data: Annotated[bytes, File()]) -> List[Transaction]:
    """
    The file you choose for '''data''' in the request body should contain lines like
    these:
     
    ```
    2020-07-01, Expense, 18.77, Fuel
    2020-07-04, Income, 40.00, 347 Woodrow
    ```
    """
    return add_transactions(data) 

@app.get("/report", name='Get a summary report')
def handle_get_report() -> Report:
    return make_report()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)