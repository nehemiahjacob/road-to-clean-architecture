import csv
import os
from datetime import date

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

    def update_balance(self, account_nr, balance):
        csv_rows = []
        with open(self.filename, "r") as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=self.field_names)
            for row in reader:
                if row["account_nr"] == account_nr:
                    row["balance"] = balance
                csv_rows.append(row)
        
        with open(self.filename, "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.field_names)
            for row in csv_rows:
                writer.writerow(row)

    def get_balance(self, account_nr):
        with open(self.filename, "r") as csv_file:
            reader = csv.DictReader(csv_file, fieldnames=self.field_names)

            for row in reader:
                if row["account_nr"] == account_nr:
                    balance = row["balance"]
                    return int(balance)