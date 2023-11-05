from python_libs.factory_boy.factories import TransactionFactory


def test_weird():
    transaction = TransactionFactory.create()
    assert len(transaction.account.customer.name) > 0