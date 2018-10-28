from domain.models import deposit, withdraw
from domain import constants

def validate(option, amount):
    if option not in (1, 2):
        raise ValueError("Not a valid option chosen!")
        
    if amount <= 0:
        raise ValueError("Must provide amount above $0!")

class AccountManager:
    def __init__(self, storage_svc, presenter):
        self.storage_svc = storage_svc
        self.presenter = presenter
    
    def open_new_account(self, account_nr, initial_balance):
        self.storage_svc.create_account(account_nr, initial_balance)

    def show_balance_and_options(self, account_nr):
        balance = self.storage_svc.get_balance(account_nr)
        self.presenter.display_options(account_nr, balance)

    def process(self, account_nr, option, amount):
        validate(option, amount)
        balance = self.storage_svc.get_balance(account_nr)
        new_balance = self._perform_transaction(balance, option, amount)
        self.storage_svc.update_balance(account_nr, new_balance)
    
    def _perform_transaction(self, balance, option, amount):
        if option == 1:
            new_balance, change, message = deposit(balance, amount)
            if message == constants.DEPOSIT_NOT_ALLOWED:
                self.presenter.notify_no_more_deposits_allowed(change)
            elif message == constants.ACCOUNT_LIMIT_REACHED:
                self.presenter.notify_account_limit_reached(change)
            elif message == constants.BALANCE_INCREASED:
                pass
            else:
                raise Exception("Unknown deposit state!")
            return new_balance
        elif option == 2:
            new_balance, message = withdraw(balance, amount)
            if message == constants.NOT_ENOUGH_MONEY:
                self.presenter.notify_overdraw_not_allowed()
            else if message == constants.BALANCE_DECREASED:
                return new_balance
            else:
                raise Exception("Unknown withdraw state!")