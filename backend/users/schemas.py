import typing
from uuid import UUID, uuid4

from common.adapters import PhoneNumberAdapter
from pydantic import BaseModel, Field


class UserCreateData(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    first_name: str
    phone_number: PhoneNumberAdapter
    is_subscribed: bool = True
    is_registered: bool = False


class UserAuthData(BaseModel):
    phone_number: PhoneNumberAdapter


class UserConfirmData(BaseModel):
    auth_code: str
