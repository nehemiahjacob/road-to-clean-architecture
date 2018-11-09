import factory
from constants import DEPOSIT_CHOSEN, WITHDRAWAL_CHOSEN
from application.requests import Deposit, Withdraw
from application.use_cases import AccountManagementUseCase

def choose_transaction(account_nr):
    option = int(input("Choose option: "))
    amount = int(input("Choose amount: "))

    if option == DEPOSIT_CHOSEN:
        return Deposit(account_nr, amount)
    elif option == WITHDRAWAL_CHOSEN:
        return Withdraw(account_nr, amount)
    else:
        raise ValueError("Unknown option selected!")

def main():
    use_case = AccountManagementUseCase()
    
    account_nr = input("Please give an account nr to create a new account: ")

    use_case.create_account(account_nr)

    while True:
        try:
            use_case.present_transaction_options(account_nr)
            transaction = choose_transaction(account_nr)
            use_case.process_transaction(transaction)
        except KeyboardInterrupt:
            print("Exiting application!")
            break
        except ValueError as ex:
            print(ex)


if __name__ == '__main__':
    main()
