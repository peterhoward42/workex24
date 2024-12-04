from models.transaction import TransactionDB

module_scope_store: list[TransactionDB] = []


def store_transactions(transactions: list[TransactionDB]):
    # We are making the assumption that the incoming transactions should
    # be stored in place of any previously stored.
    clear_storage()
    module_scope_store.extend(transactions)


def retrieve_transactions() -> list[TransactionDB]:
    return module_scope_store


def clear_storage():
    module_scope_store.clear()
