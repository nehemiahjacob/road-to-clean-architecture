import factory
from constants import DEPOSIT_CHOSEN, WITHDRAWAL_CHOSEN
from domain.models import deposit, withdraw

def process_transaction(account_nr, balance):
    option = int(input("Choose option: "))
    amount = int(input("Choose amount: "))

    if amount <= 0:
        raise ValueError("Must provide amount above $0!")

    if option == DEPOSIT_CHOSEN:
        return deposit(balance, amount)
    elif option == WITHDRAWAL_CHOSEN:
        return withdraw(balance, amount)
    else:
        raise ValueError("Unknown option selected!")

def main():
    presenter = factory.create_presenter()
    storage_svc = factory.create_storage()
    
    account_nr = input("Please give an account nr to create a new account: ")

    storage_svc.create_account(account_nr, initial_balance=0)

    while True:
        try:
            balance = storage_svc.get_balance(account_nr)
            presenter.display_options(account_nr, balance)

            invoice = process_transaction(account_nr, balance)

            storage_svc.update_balance(account_nr, invoice.current_balance)
            presenter.present(invoice)

        except KeyboardInterrupt:
            print("Exiting application!")
            break
        except ValueError as ex:
            print(ex)


if __name__ == '__main__':
    main()
