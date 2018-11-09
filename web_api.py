import graphene
import responder
from application.requests import Deposit, Withdraw
from factory import create_account_management_use_case

use_case = create_account_management_use_case()
api = responder.API()

class DepositInvoiceQL(graphene.ObjectType):
    updated_balance = graphene.Int(required=True)
    change = graphene.Int(required=True)
    description = graphene.String(required=True)

class CreateDeposit(graphene.Mutation):
    class Arguments:
        account_nr = graphene.String()
        amount = graphene.Int()

    ok = graphene.Boolean()
    invoice = graphene.Field(lambda: DepositInvoiceQL)
    
    def mutate(self, info, account_nr, amount):
        transaction = Deposit(account_nr, amount)
        fact = use_case.process_transaction(transaction)

        invoice = DepositInvoiceQL(
            updated_balance=fact.current_balance,
            change=fact.change,
            description=fact.description
        )
        return CreateDeposit(ok=True, invoice=invoice)

class WithdrawalInvoiceQL(graphene.ObjectType):
    updated_balance = graphene.Int(required=True)
    amount_withdrawn = graphene.Int(required=True)
    description = graphene.String(required=True)

class CreateWithdrawal(graphene.Mutation):
    class Arguments:
        account_nr = graphene.String()
        amount = graphene.Int()

    ok = graphene.Boolean()
    invoice = graphene.Field(lambda: WithdrawalInvoiceQL)

    def mutate(self, info, account_nr, amount):
        transaction = Withdraw(account_nr, amount)
        fact = use_case.process_transaction(transaction)

        invoice = WithdrawalInvoiceQL(
            updated_balance=fact.current_balance,
            amount_withdrawn=fact.amount_withdrawn,
            description=fact.description
        )
        return CreateWithdrawal(ok=True, invoice=invoice)

class MyMutations(graphene.ObjectType):
    create_deposit = CreateDeposit.Field()
    create_withdrawal = CreateWithdrawal.Field()

class AccountsQL(graphene.ObjectType):
    date_opened = graphene.Date(required=True)
    account_nr = graphene.String(required=True)
    balance = graphene.Int(required=True)

class Query(graphene.ObjectType):
    accounts = graphene.List(AccountsQL)

    def resolve_accounts(self, info):
        accounts_ql = map(lambda ac: AccountsQL(
            date_opened=ac.date_opened,
            account_nr=ac.account_nr,
            balance=ac.balance
        ), use_case.get_all_accounts())
        return list(accounts_ql)

schema = graphene.Schema(query=Query, mutation=MyMutations)
view = responder.ext.GraphQLView(api=api, schema=schema)

api.add_route("/", view)

if __name__ == '__main__':
    api.run()
