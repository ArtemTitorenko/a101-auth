from common.adapters import PhoneNumberAdapter
from pydantic import BaseModel


class SignUpData(BaseModel):
    first_name: str
    phone_number: PhoneNumberAdapter
    is_subscribed: bool = True


class AuthData(BaseModel):
    phone_number: PhoneNumberAdapter


class AuthConfirmData(BaseModel):
    auth_code: str
