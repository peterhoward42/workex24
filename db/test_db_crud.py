import datetime

import pytest
from sqlmodel import Session
from models.transaction import IncomeOrExpense, TransactionDBModel
from db.db_crud import clear, retrieve_transactions, store_transactions
from db.db_config import SessionDep, get_session


@pytest.fixture
def cleared_session() -> Session:
    """
    Test fixture that provides a Session pointing to a cleared database.
    """
    session = get_session().__next__()
    clear(session)
    session.commit()
    return session


def test_store_and_retrieve_happy_path(cleared_session):
    # insert 2 rows
    stored = store_transactions(make_test_transactions(), cleared_session)
    cleared_session.commit()
    assert len(stored) == 2
    assert isinstance(stored[1], TransactionDBModel)

    # Make sure they can be retrieved.
    fetched = retrieve_transactions(cleared_session)
    assert len(fetched) == 2
    assert isinstance(fetched[1], TransactionDBModel)


def test_clear(cleared_session):
    # First put some rows in.
    stored = store_transactions(make_test_transactions(), cleared_session)
    cleared_session.commit()

    # Make sure it clears them
    n_cleared = clear(cleared_session)
    cleared_session.commit()
    assert n_cleared == 2


def test_store_transactions_error_path(cleared_session):
    transactions = make_test_transactions()
    transactions[0].amount = "wrong type value"
    with pytest.raises(Exception) as err:
        store_transactions(transactions, cleared_session)
    expected = "1 validation error for TransactionDBModel\namount\n  Input should be a valid decimal"
    assert expected in str(err.value)


def make_test_transactions() -> list[TransactionDBModel]:
    return [
        TransactionDBModel(
            date=datetime.datetime.now().date(),
            category=IncomeOrExpense.expense,
            amount=3.14,
            memo="beer",
        ),
        TransactionDBModel(
            date=datetime.datetime.now().date(),
            category=IncomeOrExpense.income,
            amount=7654.321,
            memo="wine",
        ),
    ]
