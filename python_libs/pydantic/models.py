from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from python_libs.pydantic.enums import VendorType


class Vendor(BaseModel):
    name: str = Field(description='Name of the vendor.', max_length=64)
    national_id: str = Field(description='National id of the vendor.', max_length=32, default='NOT SUPPLIED')
    verification_digit: Optional[str] = Field(description='Verification digit of the National Id.', max_length=2)
    vendor_type: VendorType = Field(description='Type of vendor i.e. person or company.', default=VendorType.COMPANY)


class Receipt(BaseModel):
    vendor: Vendor = Field(description='Vendor of the receipt.')
    date: datetime = Field(description='Date of the receipt.')
    amount: Decimal = Field(description='Total amount of the receipt.', gt=Decimal('0.00'))
    tax: Decimal = Field(description='Tax for the receipt', default='0.00')
