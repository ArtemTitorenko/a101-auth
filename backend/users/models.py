from uuid import UUID

from common.adapters import PhoneNumberAdapter
from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    first_name: str
    phone_number: PhoneNumberAdapter
    is_subscribed: bool
    is_authenticated: bool
    is_registered: bool

    class Config:
        orm_mode = True
