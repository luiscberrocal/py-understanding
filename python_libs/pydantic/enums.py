from enum import Enum


class VendorType(str, Enum):
    PERSON = 'PERSON'
    COMPANY = 'COMPANY'


class Country(str, Enum):
    PANAMA = 'PA'
    COLOMBIA = 'CO'
    MEXICO = 'MX'
