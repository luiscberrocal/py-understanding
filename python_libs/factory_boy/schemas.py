from datetime import datetime

from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    national_id: str
    country: str


class Account(BaseModel):
    customer: Customer
    account_number: str


class Transaction(BaseModel):
    account: Account
    amount: float
    date: datetime
