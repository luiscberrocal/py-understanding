from _decimal import Decimal
from datetime import datetime

from python_libs.pydantic.models import Vendor, Receipt


def test_create_receipt():
    """Shows that even though the amount are supplied as text and float."""
    vendor = Vendor(name='Wayne Enterprises', national_id='4555-55-5555', verification_digit='44')
    ts = datetime.now()
    # Using string for amount
    receipt = Receipt(vendor=vendor, date=ts, amount='125.00')
    assert isinstance(receipt.amount, Decimal)
    # Using float for amount
    receipt2 = Receipt(vendor=vendor, date=ts, amount=25.45)
    assert isinstance(receipt2.amount, Decimal)


def test_create_receipt_date():
    date_strs = ['2022-09-08 16:45:55', '2022-04-11T17:11:53-05:00', '2023-04-15 16:45']

    vendor = Vendor(name='Wayne Enterprises', national_id='4555-55-5555', verification_digit='44')
    for dt in date_strs:
        receipt = Receipt(vendor=vendor, date=dt, amount='125.00')
        assert isinstance(receipt.date, datetime)
