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

def deposit(balance, amount):
    if balance >= constants.ACCOUNT_LIMIT:
        return DepositInvoice(balance, amount, constants.DEPOSIT_NOT_ALLOWED)
    elif balance + amount > constants.ACCOUNT_LIMIT:
        difference = constants.ACCOUNT_LIMIT - balance
        assert(difference <= amount)
        balance = constants.ACCOUNT_LIMIT
        change = amount - difference
        return DepositInvoice(balance, change, constants.ACCOUNT_LIMIT_REACHED)
    else:
        balance += amount
        return DepositInvoice(balance, 0, constants.BALANCE_INCREASED)
    return balance

def withdraw(balance, amount):
    if balance - amount < 0:
        return WithdrawalInvoice(balance, 0, constants.NOT_ENOUGH_MONEY)
    else:
        return WithdrawalInvoice(balance - amount, amount, constants.BALANCE_DECREASED)
