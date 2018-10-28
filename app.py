from infrastructure.persistence import StorageCSV, DatabaseStorage
from config import environment

def create_storage():
    if environment == "production":
        conn_str = "some connstring"
        return DatabaseStorage(conn_str)
    else:
        filename = "accounts.csv"
        return StorageCSV(filename)

def main():
    storage_svc = create_storage()
    account_nr = input("Please give an account nr to create a new account: ")

    initial_balance = 0
    storage_svc.create_account(account_nr, initial_balance)

    while True:
        try:
            balance = storage_svc.get_balance(account_nr)
            print("")
            print("Your current balance for #{} is ${}".format(account_nr, balance))
            print("1) Deposit money into account")
            print("2) Withdraw money from account")
            opt = int(input("Choose option: "))

            if opt not in (1, 2):
                raise ValueError("Not a valid option chosen!")

            amount = int(input("Choose amount: "))

            if amount <= 0:
                raise ValueError("Must provide amount above $0!")

            if opt == 1:
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
            elif opt == 2:
                if balance - amount < 0:
                    print("Cannot withdraw more than your current balance!")
                else:
                    balance -= amount
            
            storage_svc.update_balance(account_nr, balance)

        except KeyboardInterrupt:
            print("Exiting application!")
            break
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()
