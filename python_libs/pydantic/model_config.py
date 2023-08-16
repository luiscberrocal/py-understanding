from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


# https://docs.pydantic.dev/1.10/usage/model_config/
class Data(BaseModel):
    auth: str = Field(default='00000000')
    store: str = Field(default='NOSTORE')
    ticket: str
    partial: str = 'T'
    metadata: Any = None
    client_name: str = Field(..., alias='clientName')
    message_ticket: str = Field(alias='messageTicket', default='Sent to FE via script')

    class Config:
        allow_population_by_field_name = True


class Payload(BaseModel):
    data: Optional[Data] = None
    type: str = 'PAYMENT'
    folio: Optional[str] = None
    amount: float = None
    account: Optional[str] = None
    event_date: Optional[str] = Field(default='0', alias='eventDate')
    reference: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
