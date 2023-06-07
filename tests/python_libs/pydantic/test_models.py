from _decimal import Decimal
from datetime import datetime

from python_libs.pydantic.models import Vendor, Receipt


def test_create_receipt():
    """Shows that even though the amount are supplied as text and float."""
    vendor = Vendor(name='Wayne Enterprises', national_id='4555-55-5555', verification_digit='44')
    ts = datetime.now()
    receipt = Receipt(vendor=vendor, date=ts, amount='125.00')
    assert isinstance(receipt.amount, Decimal)
    print(receipt)
    receipt2 = Receipt(vendor=vendor, date=ts, amount=25.45)
    assert isinstance(receipt2.amount, Decimal)
