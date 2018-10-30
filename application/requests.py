
class Transaction:
    def validate(self):
        if self.amount <= 0:
            raise ValueError("Must provide amount above $0!")

class DepositMoney(Transaction):
    def __init__(self, account_nr, amount):
        self.account_nr = account_nr
        self.amount = amount

class WithdrawMoney(Transaction):
    def __init__(self, account_nr, amount):
        self.account_nr = account_nr
        self.amount = amount