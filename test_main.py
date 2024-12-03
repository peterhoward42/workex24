from decimal import Decimal

from fastapi.testclient import TestClient

from main import app
from storage.in_memory_store import retrieve_transactions, clear_storage

client = TestClient(app)


"""
Tests for /transactions
"""


def test_post_transactions_happy_path():
    clear_storage()

    # Post a simple two-line csv payload.
    files = {"data": two_line_csv_file}

    response = client.post("/transactions", files=files)

    # Check response is what is expected.
    assert response.status_code == 201
    expected = [
        {
            "date": "2020-07-01",
            "category": "Expense",
            "amount": "18.77",
            "memo": "Fuel§",
        },
        {
            "date": "2020-07-04",
            "category": "Income",
            "amount": "40.00",
            "memo": "347 Woodrow",
        },
    ]
    assert response.json() == expected

    # Check the transactions got stored.
    stored = retrieve_transactions()
    assert stored[1].amount == Decimal("40.00")


def test_post_transactions_returns_errors():
    clear_storage()

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
    clear_storage()

    # We have to load some transactions for the /report endpoint to work.
    files = {"data": two_line_csv_file}
    response = client.post("/transactions", files=files)
    assert response.status_code == 201

    # Now test the /report endpoint
    response = client.get("/report")

    assert response.status_code == 200
    expected = {"gross_revenue": "40.00", "expenses": "18.77", "net_revenue": "21.23"}
    assert response.json() == expected


def test_get_report_returns_errors():
    clear_storage()

    response = client.get("/report")

    assert response.status_code == 400
    expected = {
        "detail": "Cannot generate report because there are no stored transactions - use the /transactions endpoint to put some in."
    }
    assert response.json() == expected


two_line_csv_file = """
    2020-07-01, Expense, 18.77, Fuel§
    2020-07-04, Income, 40.00, 347 Woodrow
"""
