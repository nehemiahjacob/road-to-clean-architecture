from domain.models import Account

class DatabaseStorage:
    def __init__(self, conn_str):
        self.conn_str = conn_str

    def create_account(self, account_nr, initial_balance):
        # to implement with production DB
        return Account(account_nr, initial_balance)

    def update_account(self, account):
        # to implement with production DB
        pass

    def get_account_by_id(self, account_nr):
        # to implement with production DB
        return Account("1234", 49)

    def get_all_accounts(self):
        return []