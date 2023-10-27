import random
from datetime import datetime

from factory import Factory, SubFactory, Sequence, LazyFunction

from python_libs.factory_boy.schemas import Customer, Account, Transaction


# Pydantic Models are given in your question...

# FactoryBoy Factories:

class CustomerFactory(Factory):
    class Meta:
        model = Customer

    name = Sequence(lambda n: f'Customer {n}')
    national_id = Sequence(lambda n: f'ID{n}')
    country = "USA"


class AccountFactory(Factory):
    class Meta:
        model = Account

    customer = SubFactory(CustomerFactory)
    account_number = Sequence(lambda n: f'ACC-{n:05}')


class TransactionFactory(Factory):
    class Meta:
        model = Transaction

    account = SubFactory(AccountFactory)
    amount = LazyFunction(lambda: round(random.uniform(1, 1000), 2))
    date = LazyFunction(datetime.now)


if __name__ == '__main__':
    transaction = TransactionFactory.create()
    assert transaction.account.customer.name
