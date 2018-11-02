import graphene
import responder
from domain.models import deposit, withdraw
from factory import create_presenter, create_storage

storage_svc = create_storage()
presenter = create_presenter()
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
        if amount <= 0:
            raise ValueError("Must provide amount above $0!")
        
        balance = storage_svc.get_balance(account_nr)
        fact = deposit(balance, amount)
        storage_svc.update_balance(account_nr, fact.current_balance)
        presenter.present(fact)

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
        if amount <= 0:
            raise ValueError("Must provide amount above $0!")

        balance = storage_svc.get_balance(account_nr)
        fact = withdraw(balance, amount)
        storage_svc.update_balance(account_nr, fact.current_balance)
        presenter.present(fact)

        invoice = WithdrawalInvoiceQL(
            updated_balance=fact.current_balance,
            amount_withdrawn=fact.amount_withdrawn,
            description=fact.description
        )
        return CreateWithdrawal(ok=True, invoice=invoice)

class MyMutations(graphene.ObjectType):
    create_deposit = CreateDeposit.Field()
    create_withdrawal = CreateWithdrawal.Field()

class Query(graphene.ObjectType):
    accounts = graphene.String(account_nr=graphene.String())

    def resolve_accounts(self, info, account_nr):
        balance = use_case.show_balance_and_options(account_nr)
        return {
            "account_nr": account_nr,
            "balance": balance
        }

schema = graphene.Schema(query=Query, mutation=MyMutations)
view = responder.ext.GraphQLView(api=api, schema=schema)

api.add_route("/", view)

if __name__ == '__main__':
    api.run()
