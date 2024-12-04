import datetime
from decimal import Decimal

import pytest
from models.transaction import IncomeOrExpense, TransactionDB, TransactionCreate
from .add_transactions import build_transactions, parse_transaction

"""
tests for parse_transaction()
"""


def test_parse_transaction_happy_path():
    transaction = parse_transaction("2020-07-01, Expense, 18.77, Fuel")
    assert transaction == TransactionCreate(
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
    expectedA = "400: Cannot parse one of the CSV lines. Details: 1 validation error for TransactionCreate\ncategory"
    expectedB = "Input should be 'Income' or 'Expense' [type=enum, input_value='XXXX', input_type=str]"
    assert expectedA in str(err.value)
    assert expectedB in str(err.value)


"""
tests for build_transactions()
"""


def test_build_transactions_happy_path():
    csv = b"""
            2020-07-01, Expense, 18.77, Fuel
            2020-07-04, Income, 40.00, 347 Woodrow
        """
    transactions = build_transactions(csv)
    assert len(transactions) == 2
    assert isinstance(transactions[0], TransactionCreate)


def test_build_transactions_copes_with_whitespace_etc():
    csv = b"""
            2020-07-01, Expense, 18.77, Fuel
            
            \t
            2020-07-04, Income, 40.00, 347 Woodrow
        """
    transactions = build_transactions(csv)
    assert len(transactions) == 2
    assert isinstance(transactions[0], TransactionCreate)


def test_build_transactions_utf_encoding_problem():
    csv = bytes([0xFF, 0x00])
    with pytest.raises(Exception) as err:
        build_transactions(csv)
    expected = "400: Cannot decode your CSV input. Details: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte"
    assert expected in str(err.value)
