from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from db.db_crud import retrieve_transactions
from main import app
from models.transaction import TransactionDBModel

# from storage.in_memory_store import retrieve_transactions, clear_storage

client = TestClient(app)


"""
Tests for /transactions
"""


def test_post_transactions_happy_path():
    # Post a simple two-line csv payload.
    files = {"data": two_line_csv_file}

    response = client.post("/transactions", files=files)

    # Check response is what is expected.
    assert response.status_code == 201

    # Should be two items
    the_json = response.json()

    assert len(the_json) == 2

    # Check a sample from the list of transactions in the response,
    # can be round-trip validated into a TransactionDBModel.
    #
    # It will throw an exception if the validation fails.
    sample = the_json[1]
    TransactionDBModel.model_validate(sample)


def test_post_transactions_returns_errors():
    # clear_storage()

    # Post a malformed csv payload.
    files = {"data": "this is, malformed csv"}
    response = client.post("/transactions", files=files)

    # Check response is what is expected.
    assert response.status_code == 400
    expected = {"detail": "Should be 4 fields, not 2 (this is, malformed csv)"}
    assert response.json() == expected


"""
Tests for /report
"""


def test_get_report_happy_path():
    # We have to load some transactions for the /report endpoint to work.
    files = {"data": two_line_csv_file}
    response = client.post("/transactions", files=files)
    assert response.status_code == 201

    # Now test the /report endpoint
    response = client.get("/report")

    assert response.status_code == 200
    a = response.json()
    expected = {
        "gross_revenue": "40.0000000000",
        "expenses": "18.7700000000",
        "net_revenue": "21.2300000000",
    }
    assert response.json() == expected


def test_get_report_returns_errors():
    # We have to re initialise the database to empty by posting an empty transaction
    # payload first.
    files = {"data": ""}
    response = client.post("/transactions", files=files)
    assert response.status_code == 201

    # Now try get /report to make sure it errors.
    response = client.get("/report")

    assert response.status_code == 400
    expected = {
        "detail": "Cannot generate report because there are no stored transactions - use the /transactions endpoint to put some in."
    }
    assert response.json() == expected


two_line_csv_file = """
    2020-07-01, Expense, 18.77, Fuel
    2020-07-04, Income, 40.00, 347 Woodrow
"""
