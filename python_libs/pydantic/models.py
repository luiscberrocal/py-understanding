from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, validator

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
    source_file: Optional[Path] = Field(description='Receipt file')

    class Config:
        arbitrary_types_allowed = True

    @validator('source_file')
    def check_if_file_exists(cls, value):
        if value:
            if not value.exists():
                message = 'source_file does not exist'
                raise ValueError(message)
        return value


class GetInput(BaseModel):
    rank: Optional[int] = None
    interval: Optional[int] = None
    source_file: Optional[Path] = Field(description='Receipt file')

    @validator("rank")
    def check_range(cls, v):
        if v:
            if not 0 < v < 1000001:
                raise ValueError("Value Must be within range (0,1000000)")
            return v

    @validator('source_file')
    def force_value(cls, v):
        if v is not None:
            if not v.exists():
                raise ValueError(f'File not found {v}')
