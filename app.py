from datetime import date
import csv
import os


def main():
    filename = "accounts.csv"
    file_exists = os.path.isfile(filename)

    field_names = ["account_nr", "date_opened", "balance"]
    with open(filename, "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        if not file_exists:
            writer.writeheader()
    
    ac_nr = input("Please give an account nr to create a new account: ")

    with open(filename, "r") as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=field_names)

        for row in reader:
            if row["account_nr"] == ac_nr:
                raise ValueError("Account number already exists!")

    with open(filename, "a") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        writer.writerow({
            "account_nr": ac_nr,
            "date_opened": date.today(),
            "balance": 0
        })

    balance = 0

    while True:
        try:
            print("")
            print("Your current balance for #{} is ${}".format(ac_nr, balance))
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
            
            csv_rows = []
            with open(filename, "r") as csv_file:
                reader = csv.DictReader(csv_file, fieldnames=field_names)
                for row in reader:
                    if row["account_nr"] == ac_nr:
                        row["balance"] = balance
                    csv_rows.append(row)
            
            with open(filename, "w") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=field_names)
                for row in csv_rows:
                    writer.writerow(row)

        except KeyboardInterrupt:
            print("Exiting application!")
            break
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    main()