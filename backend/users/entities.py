from uuid import uuid4

from database import Base
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy_utils import PhoneNumberType


class UserDb(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    first_name = Column(String(length=30), nullable=False)
    phone_number = Column(PhoneNumberType(), nullable=True, unique=True)
    is_subscribed = Column(Boolean, default=False)
    is_authenticated = Column(Boolean, default=False)
    is_registered = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
