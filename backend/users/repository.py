import typing
from uuid import UUID

from database import get_db
from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .entities import UserDb
from .exceptions import UserAlreadyExistsError
from .models import User
from .schemas import UserCreateData


class UserRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session if session else get_db()

    def _get_user(self, user_id: UUID) -> typing.Optional[UserDb]:
        user = self.session.query(UserDb).filter(UserDb.id == user_id).first()
        return user if user else None

    def get(self, user_id: UUID) -> typing.Optional[User]:
        user_db = self._get_user(user_id)
        return User.from_orm(user_db) if user_db else None

    def get_by_phone_number(self, phone_number: str) -> typing.Optional[User]:
        user = (
            self.session.query(UserDb)
            .filter(UserDb.phone_number == phone_number)
            .first()
        )
        return User.from_orm(user)

    def create(self, user_data: UserCreateData) -> User:
        user_exists = (
            self.session.query(UserDb)
            .filter(UserDb.phone_number == user_data.phone_number)
            .count()
        )
        if user_data.phone_number and user_exists:
            raise UserAlreadyExistsError("Пользователь уже зарегистрирован")

        user = UserDb(**user_data.dict())
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return User.from_orm(user)

    def delete(self, user_id: UUID) -> None:
        user = self._get_user(user_id)
        if not user:
            return
        self.session.delete(user)
        self.session.commit()

    def update_phone_number(self, user_id: UUID, phone_number: str) -> User:
        user = self.session.query(UserDb).filter(UserDb.id == user_id).first()
        user.phone_number = phone_number
        self.session.commit()
        return User.from_orm(user)

    def update(self, user_id: UUID, update_data: BaseModel) -> User:
        user = self._get_user(user_id)
        for field, value in update_data.dict(exclude_unset=True, exclude_none=True).items():
            setattr(user, field, value)
        self.session.commit()
        return User.from_orm(user)

    def auth(self, user_id: UUID):
        user = self._get_user(user_id)
        user.is_authenticated = True
        user.is_registered = True

        self.session.commit()
        self.session.refresh(user)
        return user
