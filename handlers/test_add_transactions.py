import datetime
from decimal import Decimal

from fastapi import HTTPException
import pytest
from models.transaction import IncomeOrExpense, Transaction
from .add_transactions import build_transactions, parse_transaction

"""
parse_transaction() tests
"""


def test_parse_transaction_happy_path():
    transaction = parse_transaction("2020-07-01, Expense, 18.77, Fuel")
    assert transaction == Transaction(
        date=datetime.date(2020, 7, 1),
        category=IncomeOrExpense.expense,
        amount=Decimal("18.77"),
        memo="Fuel",
    )


def test_parse_transaction_fewer_than_four_fields():
    with pytest.raises(Exception) as err:
        parse_transaction("foo, bar, baz")
    assert "400: Should be 4 fields, not 3 (foo, bar, baz)" in str(err.value)


def test_parse_transaction_malformed_field():
    with pytest.raises(Exception) as err:
        parse_transaction("2020-07-01, XXXX, 18.77, Fuel")
    a = str(err.value)
    expected = "400: Cannot parse one of the CSV lines. Details: 1 validation error for Transaction\ncategory\n  Input should be 'Income' or 'Expense'"
    assert expected in str(err.value)


"""
build_transactions() tests
"""


def test_build_transactions_happy_path():
    csv = b"""
            2020-07-01, Expense, 18.77, Fuel
            2020-07-04, Income, 40.00, 347 Woodrow
        """
    transactions = build_transactions(csv)
    assert len(transactions) == 2
    assert isinstance(transactions[0], Transaction)


def test_build_transactions_copes_with_whitespace_etc():
    csv = b"""
            2020-07-01, Expense, 18.77, Fuel
            
            \t
            2020-07-04, Income, 40.00, 347 Woodrow
        """
    transactions = build_transactions(csv)
    assert len(transactions) == 2
    assert isinstance(transactions[0], Transaction)


def test_build_transactions_utf_encoding_problem():
    csv = bytes([1, 2, 3])
    with pytest.raises(Exception) as err:
        build_transactions(bytes)
    assert "400: Cannot decode your CSV input" in str(err.value)
