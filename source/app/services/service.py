from typing import List, Generic, TypeVar, Type

from app.database import Database
from app.exceptions import NotFoundException
from app.models import BaseModel


T = TypeVar("T", bound="BaseModel")


class BaseService(Generic[T]):
    def __init__(self, database: Database, model: Type[T]) -> None:
        self.database = database
        self.model = model

    def get_all(self) -> List[T]:
        with self.database.session() as session:
            entites = session.query(self.model).all()
            return entites

    def get_by_id(self, model_id: int) -> T:
        with self.database.session() as session:
            return (session
                    .query(self.model)
                    .where(self.model.id == model_id)
                    .first()
                    )

    def add(self, entity: T) -> T:
        with self.database.session() as session:
            try:
                session.add(entity)
                session.commit()
            except Exception as e:
                session.rollback()
                raise e

            return (session
                    .query(self.model)
                    .where(self.model.id == entity.id)
                    .first())

    def delete_by_id(self, model_id: int) -> bool:
        with self.database.session() as session:
            deleted = (session
                       .query(self.model)
                       .where(self.model.id == model_id)
                       .one_or_none()
                       )

            if deleted is None:
                raise NotFoundException(model_id)

            session.delete(deleted)
            session.commit()

        return True
