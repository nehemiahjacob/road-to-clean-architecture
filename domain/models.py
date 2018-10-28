def deposit(balance, amount):
    if balance >= 1000:
        return balance, amount
    elif balance + amount > 1000:
        difference = 1000 - balance
        assert(difference <= amount)
        balance = 1000
        change = amount - difference
        return balance, change
    else:
        balance += amount
        return balance, 0
    return balance

def withdraw(balance, amount):
    if balance - amount < 0:
        return balance
    else:
        return balance - amount