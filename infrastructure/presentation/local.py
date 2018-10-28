class ConsolePresenter:
    def display_options(self, account_nr, balance):
        print("")
        print("Your current balance for #{} is ${}".format(account_nr, balance))
        print("1) Deposit money into account")
        print("2) Withdraw money from account")