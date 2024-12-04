from sqlmodel import Session, SQLModel, create_engine

from models.transaction import TransactionDB, TransactionCreate, TransactionPublic

from sqlalchemy.orm import sessionmaker


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def migrate_db():
    """
    This function MUST be placed in a scope where the SQLModel classes like Transaction etc. have
    ALREADY been defined - because I believe the SQLModel.metadata (class variable) only gets
    to know which SQLModel classes it must create tables for in the database. (I tried it elsewhere,
    but then the metadata had an empty table list).
    """
    SQLModel.metadata.create_all(engine)


# TODO remove this
def get_session():
    with Session(engine) as session:
        yield session


def store_transactions(
    transactions: list[TransactionCreate], session: Session
) -> list[TransactionPublic]:
    a = 1
    response_transactions: list[TransactionPublic] = []
    for transaction in transactions:
        print(f"XXX TODO storing {repr(transaction)}")

        # TODO see what bubbling exception does before catch it
        db_transaction = TransactionDB.model_validate(transaction)
        print(f"XXX TODO validated to db_trasaction {repr(db_transaction)}")

        # Does the commit to the database inside the loop break the SQL transaction lifespan.
        # I.e. can we commit some TransactionDB rows to the database but not all if an error occurs?
        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction)
        print(f"XXX TODO value after refresh {repr(db_transaction)}")

        # TODO suspect there is a cleaner way to type coerce the transaction type below.
        t = db_transaction
        response_transaction = TransactionPublic(
            date=t.date, category=t.category, amount=t.amount, memo=t.memo, id=t.id
        )
        response_transactions.append(response_transaction)
    return response_transactions
