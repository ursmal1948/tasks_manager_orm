from abc import ABC, abstractmethod

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, delete
from typing import Any
import logging

from app.db.configuration import sa
from app.db.entity import (
    UserEntity,
    ProjectEntity,
    TaskEntity,
    CommentEntity,
    TaskStatus,
    TaskHistoryEntity
)

logging.basicConfig(level=logging.INFO)


class CrudRepository[T](ABC):

    @abstractmethod
    def save_or_update(self, entity: T) -> None:
        pass

    @abstractmethod
    def save_or_update_many(self, entities: list[T]) -> None:
        pass

    @abstractmethod
    def find_by_id(self, entity_id: int) -> T | None:
        pass

    @abstractmethod
    def find_all(self) -> list[T]:
        pass

    @abstractmethod
    def delete_by_id(self, entity_id: int) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass


#
#
class CrudRepositoryORM[T:sa.Model](CrudRepository):
    def __init__(self, db: SQLAlchemy, entity_type: Any) -> None:
        self.sa = db
        self.entity_type = entity_type

    def save_or_update(self, entity: T) -> None:
        self.sa.session.add(self.sa.session.merge(entity) if entity.id else entity)
        self.sa.session.commit()

    def save_or_update_many(self, entities: list[T]) -> None:
        self.sa.session.add_all(entities)
        self.sa.session.commit()

    def find_by_id(self, entity_id: int) -> T | None:
        stmt = select(self.entity_type).filter_by(id=entity_id)
        return self.sa.session.execute(stmt).scalar_one_or_none()

    def find_all(self) -> list[T]:
        stmt = select(self.entity_type)
        return self.sa.session.execute(stmt).scalars().all()

    def delete_by_id(self, entity_id: int) -> None:
        entity = self.find_by_id(entity_id)
        # if entity:
        self.sa.session.delete(entity)
        self.sa.session.commit()

    def delete_all(self) -> None:
        entities = self.find_all()
        for e in entities:
            self.sa.session.delete(e)
            self.sa.session.commit()


class UserRepository(CrudRepositoryORM[UserEntity]):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db, UserEntity)

    def find_by_name(self, name: str) -> UserEntity | None:
        return self.entity_type.query.filter_by(name=name).first()

    def find_email_by_id(self, user_id: int) -> str:
        stmt = select(self.entity_type).filter_by(id=user_id)
        return self.sa.session.execute(stmt).scalars().first().email

    def find_all_projects_for_user(self, user_id: int) -> list[ProjectEntity]:
        return self.find_by_id(user_id).projects

    def find_by_email(self, email: str) -> UserEntity | None:
        stmt = select(UserEntity).filter_by(email=email)
        return self.sa.session.execute(stmt).scalar_one_or_none()

    def find_last_added_user(self) -> UserEntity | None:
        stmt = select(self.entity_type).order_by(UserEntity.id.desc()).limit(1)
        return self.sa.session.execute(stmt).scalars().first()


class ProjectRepository(CrudRepositoryORM[UserEntity]):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db, ProjectEntity)

    # nie sprwadzilam tego jeszce.
    def find_by_name(self, name: str) -> UserEntity | None:
        stmt = select(ProjectEntity).filter_by(name=name)
        return self.sa.session.execute(stmt).scalar_one_or_none()

    def find_all_tasks_for_project(self, project_id: int) -> list[TaskEntity]:
        return self.find_by_id(project_id).tasks

    def find_user_id_by_project_id(self, project_id: int) -> str:
        return self.find_by_id(project_id).user_id

    def find_last_added_project(self) -> UserEntity | None:
        stmt = select(self.entity_type).order_by(ProjectEntity.id.desc()).limit(1)
        return self.sa.session.execute(stmt).scalars().first()


class TaskRepository(CrudRepositoryORM[TaskEntity]):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db, TaskEntity)

    def find_task_project(self, task_id: int) -> ProjectEntity:
        return self.find_by_id(task_id).project

    def find_tasks_by_status(self, status: TaskStatus) -> list[TaskEntity]:
        stmt = select(TaskEntity).filter_by(status=status.name)
        return self.sa.session.execute(stmt).scalars().all()

    def find_project_id_by_task_id(self, task_id: int) -> int:
        return self.find_by_id(task_id).project_id

    def find_task_histories_for_task(self, task_id: int) -> list[TaskHistoryEntity]:
        return self.find_by_id(task_id).task_histories


class CommentRepository(CrudRepositoryORM[CommentEntity]):

    def __init__(self, db: SQLAlchemy):
        super().__init__(db, CommentEntity)

    def find_by_content(self, content: str) -> CommentEntity | None:
        stmt = select(CommentEntity).filter_by(content=content)
        return self.sa.session.execute(stmt).scalars().first()


class TaskHistoryRepository(CrudRepositoryORM[TaskHistoryEntity]):
    def __init__(self, db: SQLAlchemy):
        super().__init__(db, TaskHistoryEntity)


user_repository = UserRepository(sa)
project_repository = ProjectRepository(sa)
task_repository = TaskRepository(sa)
comment_repository = CommentRepository(sa)
task_history_repository = TaskHistoryRepository(sa)
