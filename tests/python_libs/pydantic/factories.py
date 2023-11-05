from datetime import datetime
from decimal import Decimal
from pathlib import Path

import factory
from factory import fuzzy

from python_libs.pydantic.enums import VendorType, Country
from python_libs.pydantic.models import Vendor, Receipt, Customer, Account


# Assuming the Enums and BaseModel definitions are like this

# Factories for your models
class VendorFactory(factory.Factory):
    class Meta:
        model = Vendor

    name = factory.Faker('company')
    national_id = factory.Faker('ssn')
    verification_digit = factory.LazyFunction(lambda: str(fuzzy.FuzzyInteger(0, 99).fuzz()))
    vendor_type = VendorType.COMPANY


class ReceiptFactory(factory.Factory):
    class Meta:
        model = Receipt

    vendor = factory.SubFactory(VendorFactory)
    date = factory.LazyFunction(datetime.now)
    amount = fuzzy.FuzzyDecimal(0.01, 10000.00)
    tax = Decimal('0.00')
    source_file = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default '_create' with our custom call."""
        source_file_path = kwargs.pop('source_file', None)
        if source_file_path:
            source_file_path = Path(source_file_path)
            if not source_file_path.exists():
                raise ValueError(f'File not found {source_file_path}')
            kwargs['source_file'] = source_file_path
        return super()._create(model_class, *args, **kwargs)


class CustomerFactory(factory.Factory):
    class Meta:
        model = Customer

    name = factory.Faker('name')
    country = Country.PANAMA


class AccountFactory(factory.Factory):
    class Meta:
        model = Account

    customer = factory.SubFactory(CustomerFactory)
    country = Country.PANAMA
