import constants

class DepositInvoice:
    def __init__(self, current_balance, change, description):
        self.current_balance = current_balance
        self.change = change
        self.description = description

class WithdrawalInvoice:
    def __init__(self, current_balance, amount_withdrawn, description):
        self.current_balance = current_balance
        self.amount_withdrawn = amount_withdrawn
        self.description = description

class Account:
    def __init__(self, account_nr, balance):
        self.account_nr = account_nr
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Must provide amount above $0!")

        if self.balance >= constants.ACCOUNT_LIMIT:
            return DepositInvoice(self.balance, amount, constants.DEPOSIT_NOT_ALLOWED)
        elif self.balance + amount > constants.ACCOUNT_LIMIT:
            difference = constants.ACCOUNT_LIMIT - self.balance
            assert(difference <= amount)
            self.balance = constants.ACCOUNT_LIMIT
            change = amount - difference
            return DepositInvoice(self.balance, change, constants.ACCOUNT_LIMIT_REACHED)
        else:
            self.balance += amount
            return DepositInvoice(self.balance, 0, constants.BALANCE_INCREASED)
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Must provide amount above $0!")

        if self.balance - amount < 0:
            return WithdrawalInvoice(self.balance, 0, constants.NOT_ENOUGH_MONEY)
        else:
            self.balance -= amount
            return WithdrawalInvoice(self.balance - amount, amount, constants.BALANCE_DECREASED)
