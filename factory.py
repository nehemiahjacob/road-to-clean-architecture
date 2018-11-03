from application.use_cases import AccountManagementUseCase
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

def create_account_management_use_case():
    storage_svc = create_storage()
    presenter = create_presenter()
    return AccountManagementUseCase(storage_svc, presenter)