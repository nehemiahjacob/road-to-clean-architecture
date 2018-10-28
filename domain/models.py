def deposit(balance, amount):
    if balance >= 1000:
        print("Account limit of $1000 has been reached! Cannot deposit any more money!")
        print("Returned the ${}".format(amount))
    elif balance + amount > 1000:
        difference = 1000 - balance
        assert(difference <= amount)
        balance = 1000
        change = amount - difference
        print("You have deposited enough to reach account limit of $1000!")
        if change:
            print("Change of ${} returned".format(change))
        print("Cannot exceed account limit of $1000!")
    else:
        balance += amount
    return balance

def withdraw(balance, amount):
    if balance - amount < 0:
        print("Cannot withdraw more than your current balance!")
    else:
        balance -= amount
    return balance