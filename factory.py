from infrastructure.persistence import StorageCSV, DatabaseStorage
from infrastructure.presentation import ConsolePresenter
from application.services import AccountManager
from config import environment

def create_storage():
    if environment == "production":
        conn_str = "some connstring"
        return DatabaseStorage(conn_str)
    else:
        filename = "accounts.csv"
        return StorageCSV(filename)

def create_presenter():
    return ConsolePresenter()

def create_account_management_use_case():
    storage_svc = create_storage()
    presenter = create_presenter()
    return AccountManager(storage_svc, presenter)
    