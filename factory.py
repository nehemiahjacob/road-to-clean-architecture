from config import environment
from infrastructure.persistence import DatabaseStorage, StorageCSV
from infrastructure.presentation import ConsolePresenter


def create_storage():
    if environment == "production":
        conn_str = "some connstring"
        return DatabaseStorage(conn_str)
    else:
        filename = "accounts.csv"
        return StorageCSV(filename)

def create_presenter():
    if environment == "production":
        raise NotImplementedError()
    else:
        return ConsolePresenter()