from .constants import (ACCOUNT_LIMIT, ACCOUNT_LIMIT_REACHED,
                        BALANCE_DECREASED, BALANCE_INCREASED,
                        DEPOSIT_NOT_ALLOWED, NOT_ENOUGH_MONEY)

def deposit(balance, amount):
    if balance >= ACCOUNT_LIMIT:
        return balance, amount, DEPOSIT_NOT_ALLOWED
    elif balance + amount > ACCOUNT_LIMIT:
        difference = ACCOUNT_LIMIT - balance
        assert(difference <= amount)
        balance = ACCOUNT_LIMIT
        change = amount - difference
        return balance, change, ACCOUNT_LIMIT_REACHED
    else:
        balance += amount
        return balance, 0, BALANCE_INCREASED
    return balance

def withdraw(balance, amount):
    if balance - amount < 0:
        return balance, NOT_ENOUGH_MONEY
    else:
        return balance - amount, BALANCE_DECREASED
