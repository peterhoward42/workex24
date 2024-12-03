from models.transaction import Transaction

module_scope_store: list[Transaction] = []


def store_transactions(transactions: list[Transaction]):
    # We are making the assumption that the incoming transactions should
    # be stored in place of any previously stored.
    clear_storage()
    module_scope_store.extend(transactions)


def retrieve_transactions() -> list[Transaction]:
    return module_scope_store


def clear_storage():
    module_scope_store.clear()
