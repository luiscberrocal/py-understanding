from datetime import datetime

from pydantic import BaseModel, Field


def convert_datetime_to_iso_8601(dt: datetime) -> str:
    return dt.strftime('%Y-%m-%d %H:%M:%S')


class Contract(BaseModel):
    name: str = Field(alias='firstname')
    contract_id: str = Field(alias='ContractId')
    contract_sign_date: datetime = Field(alias='contractsigndate')

    class Config:
        allow_population_by_field_name = True


class ContractDate(BaseModel):
    name: str = Field(alias='firstname')
    contract_id: str = Field(alias='ContractId')
    contract_sign_date: datetime = Field(alias='contractsigndate')

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            # custom output conversion for datetime
            datetime: convert_datetime_to_iso_8601
        }


def build_with_str_date():
    contract = Contract(name='Luis Gonzalez', contract_id=111155,
                        contract_sign_date='2023-05-01 16:15:52')
    # Notice "contract_sign_date": "2023-05-01T16:15:52"
    print(contract.json())

    contract_date = ContractDate(name='Bruce Wayne', contract_id=311155,
                                 contract_sign_date='2023-05-01 16:15:52')
    # Notice "contract_sign_date": "2023-05-01 16:15:52"
    print(contract_date.json())




if __name__ == '__main__':
    build_with_str_date()
