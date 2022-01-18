from typing import List, Optional, Union

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import Base, get_db

from .base_model import Model


class BaseService:
    model: Model
    db_model: Base

    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_by_id(self, id: int) -> Optional[Model]:
        return self.session.query(self.model).filter(self.model.id == id).one()

    def get_all(self) -> List[Base]:
        return self.session.query(self.model).all()

    def get_with_filter(
        self, data: dict, first: bool = True
    ) -> Union[Optional[Model], Optional[List[Model]]]:
        query = self.session.query(self.model)
        for field, value in data.items():
            try:
                query = query.filter(getattr(self.model, field) == value)
            except AttributeError:
                raise AttributeError(f'В данной модели не существует поля {field}')
        if first:
            return query.first()
        return query.all()

    def create_with_check(self, input_data: dict) -> Optional[Model]:
        if _ := self.get_with_filter(input_data):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)
        return self.create(input_data)

    def create(self, input_data: dict) -> Model:
        db_model = self.db_model(**input_data)
        self.session.add(db_model)
        self.session.commit()
        return self.model.from_orm(db_model)

    def update(self, db_data: Base, input_data: Model) -> Model:
        for field, value in input_data.dict(exclude_unset=True, exclude_none=True).items():
            setattr(db_data, field, value)
        self.session.commit()
        return db_data

    def delete(self, db_data: Base) -> None:
        self.session.delete(db_data)
        self.session.commit()
