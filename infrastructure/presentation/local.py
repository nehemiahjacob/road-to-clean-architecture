class ConsolePresenter:
    def display_options(self, account_nr, balance):
        print("")
        print("Your current balance for #{} is ${}".format(account_nr, balance))
        print("1) Deposit money into account")
        print("2) Withdraw money from account")
    
    def notify_no_more_deposits_allowed(self, change):
        print("Account limit of $1000 has been reached! Cannot deposit any more money!")
        print("Returned the ${}".format(change))

    def notify_account_limit_reached(self, change):
        print("You have deposited enough to reach account limit of $1000!")
        print("Change of ${} returned".format(change))
        print("Cannot exceed account limit of $1000!")

    def notify_overdraw_not_allowed(self):
        print("Cannot withdraw more than your current balance!")