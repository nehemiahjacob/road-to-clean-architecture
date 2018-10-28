from infrastructure.persistence import StorageCSV, DatabaseStorage
from config import environment

def create_storage():
    if environment == "production":
        conn_str = "some connstring"
        return DatabaseStorage(conn_str)
    else:
        filename = "accounts.csv"
        return StorageCSV(filename)
