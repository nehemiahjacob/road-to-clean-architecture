class DatabaseStorage:
    def __init__(self, conn_str):
        self.conn_str = conn_str

    def create_account(self, account_nr, balance):
        # to implement with production DB
        pass

    def update_balance(self, account_nr, balance):
        # to implement with production DB
        pass

    def get_balance(self, account_nr):
        # to implement with production DB
        return 49