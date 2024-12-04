from models.transaction import Transaction

"""
This module is a temporary placeholder implementation for a data store.
It provides ephemeral storage of data in (process) memory.
"""
module_scope_store: list[Transaction] = []


def store_transactions(transactions: list[Transaction]):
    """
    Stores the given transactions.

    We are making the assumption that the incoming transactions should
    overwrite the existing storage content.
    """
    clear_storage()
    module_scope_store.extend(transactions)


def retrieve_transactions() -> list[Transaction]:
    """
    Retrieve the stored transactions. The result can be an empty list.
    """
    return module_scope_store


def clear_storage():
    """
    Empty the current store content.
    """
    module_scope_store.clear()
