import factory

def main():
    use_case = factory.create_account_management_use_case()
    
    account_nr = input("Please give an account nr to create a new account: ")

    use_case.open_new_account(account_nr, initial_balance=0)

    while True:
        try:
            use_case.show_balance_and_options(account_nr)
                
            option = int(input("Choose option: "))
            amount = int(input("Choose amount: "))

            fact = use_case.process(account_nr, option, amount)
        except KeyboardInterrupt:
            print("Exiting application!")
            break
        except ValueError as ex:
            print(ex)


if __name__ == '__main__':
    main()
