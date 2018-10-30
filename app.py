import factory
from constants import DEPOSIT_CHOSEN, WITHDRAWAL_CHOSEN
from application.requests import DepositMoney, WithdrawMoney

def new_transaction(account_nr):
    option = int(input("Choose option: "))
    amount = int(input("Choose amount: "))
    if option == DEPOSIT_CHOSEN:
        return DepositMoney(account_nr, amount)
    elif option == WITHDRAWAL_CHOSEN:
        return WithdrawMoney(account_nr, amount)
    else:
        raise ValueError(f"Unknown option chosen {option}!")

def main():
    use_case = factory.create_account_management_use_case()
    
    account_nr = input("Please give an account nr to create a new account: ")

    use_case.open_new_account(account_nr, initial_balance=0)

    while True:
        try:
            use_case.show_balance_and_options(account_nr)

            transaction = new_transaction(account_nr)

            fact = use_case.process(transaction)
        except KeyboardInterrupt:
            print("Exiting application!")
            break
        except ValueError as ex:
            print(ex)


if __name__ == '__main__':
    main()
