import typing
from datetime import datetime

from common.adapters import PhoneNumberAdapter
from pydantic import BaseModel


class SmsVerification(BaseModel):
    id: int
    phone_number: PhoneNumberAdapter
    auth_code: typing.Optional[str]
    auth_code_tries: int
    auth_code_time: typing.Optional[datetime]
    created_at: datetime
    modified_at: typing.Optional[datetime]

    class Config:
        orm_mode = True
