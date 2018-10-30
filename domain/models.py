from .constants import (ACCOUNT_LIMIT, ACCOUNT_LIMIT_REACHED,
                        BALANCE_DECREASED, BALANCE_INCREASED,
                        DEPOSIT_NOT_ALLOWED, NOT_ENOUGH_MONEY)

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
    if balance >= ACCOUNT_LIMIT:
        return DepositInvoice(balance, amount, DEPOSIT_NOT_ALLOWED)
    elif balance + amount > ACCOUNT_LIMIT:
        difference = ACCOUNT_LIMIT - balance
        assert(difference <= amount)
        balance = ACCOUNT_LIMIT
        change = amount - difference
        return DepositInvoice(balance, change, ACCOUNT_LIMIT_REACHED)
    else:
        balance += amount
        return DepositInvoice(balance, 0, BALANCE_INCREASED)
    return balance

def withdraw(balance, amount):
    if balance - amount < 0:
        return WithdrawalInvoice(balance, 0, NOT_ENOUGH_MONEY)
    else:
        return WithdrawalInvoice(balance - amount, amount, BALANCE_DECREASED)
