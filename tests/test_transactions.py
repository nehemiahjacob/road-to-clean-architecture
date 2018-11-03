import unittest
from domain.models import Account
import constants

class AccountTests(unittest.TestCase):
    def test_deposit_money(self):
        ac = Account("123", 0)
        invoice = ac.deposit(15)
        self.assertEqual(ac.balance, 15)
        self.assertEqual(invoice.change, 0)
        self.assertEqual(invoice.current_balance, ac.balance)
    
    def test_withdraw_from_non_zero_balance(self):
        ac = Account("123", 500)
        invoice = ac.withdraw(45)
        self.assertEqual(ac.balance, 455)
        self.assertEqual(invoice.amount_withdrawn, 45)
        self.assertEqual(invoice.current_balance, ac.balance)
    
    def test_deposit_plus_balance_reaches_account_limit(self):
        ac = Account("123", 990)
        invoice = ac.deposit(12)
        self.assertEqual(ac.balance, constants.ACCOUNT_LIMIT)
        self.assertEqual(invoice.change, 2)
        self.assertEqual(invoice.current_balance, ac.balance)
    
    def test_cannot_deposit_more_account_limit_reached(self):
        ac = Account("123", 1000)
        invoice = ac.deposit(20)
        self.assertEqual(ac.balance, constants.ACCOUNT_LIMIT)
        self.assertEqual(invoice.change, 20)
        self.assertEqual(invoice.current_balance, ac.balance)
    
    def test_withdrawal_not_allowed_not_enough_balance(self):
        ac = Account("123", 99)
        invoice = ac.withdraw(100)
        self.assertEqual(ac.balance, 99)
        self.assertEqual(invoice.amount_withdrawn, 0)
        self.assertEqual(invoice.current_balance, ac.balance)
    
    def test_invalid_deposit_amount(self):
        ac = Account("123", 250)
        with self.assertRaises(ValueError):
            invoice = ac.deposit(-10)
            self.assertIsNone(invoice)
    
    def test_invalid_withdrawal_amount(self):
        ac = Account("123", 250)
        with self.assertRaises(ValueError):
            invoice = ac.withdraw(-10)
            self.assertIsNone(invoice)

if __name__ == '__main__':
    unittest.main()