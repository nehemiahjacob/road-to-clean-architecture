from domain.models import deposit, withdraw
import constants

def validate(option, amount):
    if option not in (constants.DEPOSIT_CHOSEN, constants.WITHDRAWAL_CHOSEN):
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
        invoice = self._perform_transaction(balance, option, amount)
        self.storage_svc.update_balance(account_nr, invoice.current_balance)
        self.presenter.present(invoice)
        return invoice
    
    def _perform_transaction(self, balance, option, amount):
        if option == constants.DEPOSIT_CHOSEN:
            return deposit(balance, amount)
        elif option == constants.WITHDRAWAL_CHOSEN:
            return withdraw(balance, amount)