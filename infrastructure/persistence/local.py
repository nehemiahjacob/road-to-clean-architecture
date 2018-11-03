import csv
import os
from datetime import date, datetime
from domain.models import Account

class AccountDTO:
    def __init__(self, date_opened, account_nr, balance):
        self.date_opened = date_opened
        self.account_nr = account_nr
        self.balance = balance

class StorageCSV:
    def __init__(self, filename):
        self.filename = filename
        self.field_names = ["account_nr", "date_opened", "balance"]
        self._initialize()

    def _initialize(self):
        file_exists = os.path.isfile(self.filename)
        with open(self.filename, "a") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.field_names)
            if not file_exists:
                writer.writeheader()

    def create_account(self, account_nr, initial_balance):
        with open(self.filename, "r") as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=self.field_names)

            for row in reader:
                if row["account_nr"] == account_nr:
                    raise ValueError("Account number already exists!")

        with open(self.filename, "a") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.field_names)

            writer.writerow({
                "account_nr": account_nr,
                "date_opened": date.today(),
                "balance": initial_balance
            })

        return Account(account_nr, initial_balance)

    def update_account(self, account):
        assert(account.balance >= 0)
        csv_rows = []
        with open(self.filename, "r") as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=self.field_names)
            for row in reader:
                if row["account_nr"] == account.account_nr:
                    row["balance"] = account.balance
                csv_rows.append(row)
        
        with open(self.filename, "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.field_names)
            for row in csv_rows:
                writer.writerow(row)
    
    def get_account_by_id(self, account_nr):
        with open(self.filename, "r") as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=self.field_names)

            for row in reader:
                if row["account_nr"] == account_nr:
                    balance = row["balance"]
                    return Account(account_nr, int(balance))

    def get_all_accounts(self):
        with open(self.filename, "r") as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=self.field_names)

            # skip first row, which is the header
            next(reader)

            accounts = map(lambda row: AccountDTO(
                date_opened=datetime.strptime(row["date_opened"], "%Y-%M-%d").date(),
                account_nr=row["account_nr"],
                balance=row["balance"]
            ), reader)
            return list(accounts)