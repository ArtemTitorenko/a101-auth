from database import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy_utils import PhoneNumberType


class SmsVerificationDb(Base):
    __tablename__ = "sms_verifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone_number = Column(PhoneNumberType(), nullable=False, unique=True)
    auth_code = Column(String, nullable=True)
    auth_code_tries = Column(Integer, default=0)
    auth_code_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
