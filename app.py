import factory
from constants import DEPOSIT_CHOSEN, WITHDRAWAL_CHOSEN

def process_transaction(account):
    option = int(input("Choose option: "))
    amount = int(input("Choose amount: "))

    if option == DEPOSIT_CHOSEN:
        return account.deposit(amount)
    elif option == WITHDRAWAL_CHOSEN:
        return account.withdraw(amount)
    else:
        raise ValueError("Unknown option selected!")

def main():
    presenter = factory.create_presenter()
    storage_svc = factory.create_storage()
    
    account_nr = input("Please give an account nr to create a new account: ")

    storage_svc.create_account(account_nr, initial_balance=0)

    while True:
        try:
            account = storage_svc.get_account_by_id(account_nr)
            presenter.display_options(account)

            invoice = process_transaction(account)

            storage_svc.update_account(account)
            presenter.present(invoice)

        except KeyboardInterrupt:
            print("Exiting application!")
            break
        except ValueError as ex:
            print(ex)


if __name__ == '__main__':
    main()
