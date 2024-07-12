from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import (
    Engine,
    select,
    delete
)
from sqlalchemy.orm import (
    DeclarativeBase,
    sessionmaker
)


class CrudRepository(ABC):
    @abstractmethod
    def save_or_update(self, item: Any) -> None:
        pass

    @abstractmethod
    def save_or_update_many(self, items: list[Any]) -> None:
        pass

    @abstractmethod
    def find_by_id(self, id_: int) -> Any | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Any]:
        pass

    @abstractmethod
    def delete_by_id(self, id_: int) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass


class CrudRepositoryORM(CrudRepository):
    def __init__(self, engine: Engine, entity_type: Any) -> None:
        self._engine = engine
        self._entity_type = type(entity_type())

    def save_or_update(self, item: Any) -> None:
        with self._create_session() as session, session.begin():
            session.add(session.merge(item) if item.id else item)

    def save_or_update_many(self, items: list[Any]) -> None:
        with self._create_session() as session, session.begin():
            session.add_all([
                session.merge(item) if item.id else item for item in items
            ])

    def find_by_id(self, id_: int) -> Any | None:
        with self._create_session() as session:
            stmt = select(self._entity_type).filter_by(id=id_)
            return session.execute(stmt).scalars().first()

    def find_all(self) -> list[Any]:
        with self._create_session() as session:
            stmt = select(self._entity_type)
            return session.execute(stmt).scalars().all()

    def delete_by_id(self, id_: int) -> None:
        with self._create_session() as session, session.begin():
            stmt = select(self._entity_type).filter_by(id=id_)

            item_do_delete = session.execute(stmt).scalars().first()
            if item_do_delete:
                session.delete(item_do_delete)

    def delete_all(self) -> None:
        with self._create_session() as session, session.begin():
            stmt = delete(self._entity_type).where(self._entity_type.id >= 1)
            session.execute(stmt)

    def _create_session(self):
        session = sessionmaker(bind=self._engine, expire_on_commit=False)
        return session()
