from domain.models import deposit, withdraw
import constants
from .requests import DepositMoney, WithdrawMoney

class AccountManager:
    def __init__(self, storage_svc, presenter):
        self.storage_svc = storage_svc
        self.presenter = presenter
    
    def open_new_account(self, account_nr, initial_balance):
        self.storage_svc.create_account(account_nr, initial_balance)

    def show_balance_and_options(self, account_nr):
        balance = self.storage_svc.get_balance(account_nr)
        self.presenter.display_options(account_nr, balance)

    def process(self, request_obj):
        request_obj.validate()
        balance = self.storage_svc.get_balance(request_obj.account_nr)
        invoice = None
        if request_obj.__class__ == DepositMoney:
            invoice = deposit(balance, request_obj.amount)
        elif request_obj.__class__ == WithdrawMoney:
            invoice = withdraw(balance, request_obj.amount)
        else:
            raise TypeError("Unknown request type!")
        self.storage_svc.update_balance(request_obj.account_nr, invoice.current_balance)
        self.presenter.present(invoice)
        return invoice