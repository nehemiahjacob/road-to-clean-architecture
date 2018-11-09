import unittest
from domain.models import Account
from application.use_cases import AccountManagementUseCase
from application.requests import Deposit, Withdraw
import constants

class NullPresenter:
    def present(self, fact):
        pass

class MockStorage:
    def create_account(self, account_nr, initial_balance):
        self.balance = initial_balance
    
    def get_account_by_id(self, account_nr):
        return Account(account_nr, self.balance)

    def update_account(self, account):
        self.balance = account.balance

class AccountE2ETests(unittest.TestCase):
    def test_deposit_money(self):
        use_case = AccountManagementUseCase(MockStorage(), NullPresenter())
        use_case.create_account("123")
        invoice = use_case.process_transaction(Deposit("123", 15))
        ac = use_case.get_account_by_id("123")
        self.assertEqual(ac.balance, 15)
        self.assertEqual(invoice.change, 0)
        self.assertEqual(invoice.current_balance, ac.balance)
    
    def test_withdraw_from_non_zero_balance(self):
        use_case = AccountManagementUseCase(MockStorage(), NullPresenter())
        use_case.create_account("123")
        use_case.process_transaction(Deposit("123", 500))
        invoice = use_case.process_transaction(Withdraw("123", 45))
        ac = use_case.get_account_by_id("123")
        self.assertEqual(ac.balance, 455)
        self.assertEqual(invoice.amount_withdrawn, 45)
        self.assertEqual(invoice.current_balance, ac.balance)
    
    def test_deposit_plus_balance_reaches_account_limit(self):
        use_case = AccountManagementUseCase(MockStorage(), NullPresenter())
        use_case.create_account("123")
        use_case.process_transaction(Deposit("123", 990))
        invoice = use_case.process_transaction(Deposit("123", 12))
        ac = use_case.get_account_by_id("123")
        self.assertEqual(ac.balance, constants.ACCOUNT_LIMIT)
        self.assertEqual(invoice.change, 2)
        self.assertEqual(invoice.current_balance, ac.balance)
    
    def test_cannot_deposit_more_account_limit_reached(self):
        use_case = AccountManagementUseCase(MockStorage(), NullPresenter())
        use_case.create_account("123")
        use_case.process_transaction(Deposit("123", 1000))
        invoice = use_case.process_transaction(Deposit("123", 20))
        ac = use_case.get_account_by_id("123")
        self.assertEqual(ac.balance, constants.ACCOUNT_LIMIT)
        self.assertEqual(invoice.change, 20)
        self.assertEqual(invoice.current_balance, ac.balance)
    
    def test_withdrawal_not_allowed_not_enough_balance(self):
        use_case = AccountManagementUseCase(MockStorage(), NullPresenter())
        use_case.create_account("123")
        use_case.process_transaction(Deposit("123", 99))
        invoice = use_case.process_transaction(Withdraw("123", 100))
        ac = use_case.get_account_by_id("123")
        self.assertEqual(ac.balance, 99)
        self.assertEqual(invoice.amount_withdrawn, 0)
        self.assertEqual(invoice.current_balance, ac.balance)
    
    def test_invalid_deposit_amount(self):
        use_case = AccountManagementUseCase(MockStorage(), NullPresenter())
        use_case.create_account("123")
        use_case.process_transaction(Deposit("123", 250))
        with self.assertRaises(ValueError):
            invoice = use_case.process_transaction(Deposit("123", -10))
            self.assertIsNone(invoice)
    
    def test_invalid_withdrawal_amount(self):
        use_case = AccountManagementUseCase(MockStorage(), NullPresenter())
        use_case.create_account("123")
        use_case.process_transaction(Deposit("123", 250))
        with self.assertRaises(ValueError):
            invoice = use_case.process_transaction(Withdraw("123", -10))
            self.assertIsNone(invoice)

if __name__ == '__main__':
    unittest.main()