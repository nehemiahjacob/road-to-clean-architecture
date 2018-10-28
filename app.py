import csv
import os
from datetime import date

filename = "accounts.csv"
file_exists = os.path.isfile(filename)
field_names = ["account_nr", "date_opened", "balance"]

def initialize():
    with open(filename, "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        if not file_exists:
            writer.writeheader()

def create_account(account_nr, balance):
    with open(filename, "r") as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=field_names)

        for row in reader:
            if row["account_nr"] == account_nr:
                raise ValueError("Account number already exists!")

    with open(filename, "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        writer.writerow({
            "account_nr": account_nr,
            "date_opened": date.today(),
            "balance": balance
        })

def update_balance(account_nr, balance):
    csv_rows = []
    with open(filename, "r") as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=field_names)
        for row in reader:
            if row["account_nr"] == account_nr:
                row["balance"] = balance
            csv_rows.append(row)
    
    with open(filename, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        for row in csv_rows:
            writer.writerow(row)

def get_balance(account_nr):
    with open(filename, "r") as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=field_names)

        for row in reader:
            if row["account_nr"] == account_nr:
                balance = row["balance"]
                return int(balance)

def main():
    initialize()
    account_nr = input("Please give an account nr to create a new account: ")

    initial_balance = 0
    create_account(account_nr, initial_balance)

    while True:
        try:
            balance = get_balance(account_nr)
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
            
            update_balance(account_nr, balance)

        except KeyboardInterrupt:
            print("Exiting application!")
            break
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()
