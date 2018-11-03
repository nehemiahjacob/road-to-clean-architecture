from .requests import Deposit, Withdraw

class AccountManagementUseCase:
    def __init__(self, storage_svc, presenter):
        self.storage_svc = storage_svc
        self.presenter = presenter

    def create_account(self, account_nr):
        return self.storage_svc.create_account(account_nr, initial_balance=0)

    def present_transaction_options(self, account_nr):
        account = self.storage_svc.get_account_by_id(account_nr)
        self.presenter.display_options(account)

    def process_transaction(self, request_obj):
        if request_obj.__class__ == Deposit:
            return self._handle_deposit(request_obj)
        elif request_obj.__class__ == Withdraw:
            return self._handle_withdraw(request_obj)

    def _handle_deposit(self, request_obj):
        account = self.storage_svc.get_account_by_id(request_obj.account_nr)
        fact = account.deposit(request_obj.amount)
        self.storage_svc.update_account(account)
        self.presenter.present(fact)
        return fact

    def _handle_withdraw(self, request_obj):
        account = self.storage_svc.get_account_by_id(request_obj.account_nr)
        fact = account.withdraw(request_obj.amount)
        self.storage_svc.update_account(account)
        self.presenter.present(fact)
        return fact

