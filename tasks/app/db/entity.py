from app.db.configuration import sa
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column
)
from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Numeric,
    ForeignKey
)
from decimal import Decimal
from enum import Enum
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column
)
from typing import Self
from sqlalchemy import (
    Integer,
    String,
    Numeric,
    ForeignKey
)
from decimal import Decimal


class UserEntity(sa.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(30), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(sa.String(30), nullable=False)

    projects: Mapped[list['ProjectEntity']] = sa.relationship('ProjectEntity', backref=sa.backref('user', lazy=False))

    def __str__(self) -> str:
        return f'ID: {self.id} User: {self.name} email: {self.email}'

    def __repr__(self):
        return str(self)

    def to_dict(self) -> dict[str, int | str | Decimal]:
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'email': self.email
        }


class ProjectEntity(sa.Model):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    # todo moze unique name
    name: Mapped[str] = mapped_column(sa.String(30), nullable=False)
    description: Mapped[str] = mapped_column(sa.String(30), nullable=False)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'))

    tasks: Mapped[list['TaskEntity']] = sa.relationship('TaskEntity', backref=sa.backref('project', lazy=False))

    def __str__(self) -> str:
        return f'ID: {self.id} Project: {self.name} Descirption: {self.description}'

    def __repr__(self):
        return str(self)

    def to_dict(self) -> dict[str, int | str | Decimal]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
        }


class TaskStatus(Enum):
    NEW = 0
    IN_PROGRESS = 1
    COMPLETED = 2

    def to_str(self) -> str:
        return self.name


class TaskEntity(sa.Model):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(sa.String(30), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.NEW)
    project_id: Mapped[int] = mapped_column(sa.ForeignKey('projects.id'))

    comments: Mapped[list['CommentEntity']] = sa.relationship('CommentEntity', backref=sa.backref('task', lazy=False))
    task_histories: Mapped[list['TaskHistoryEntity']] = sa.relationship('TaskHistoryEntity',
                                                                        backref=sa.backref('task', lazy=False))

    # projects: Mapped[list['ProjectEntity']] = sa.relationship('ProjectEntity', backref=sa.backref('user', lazy=False))

    def __str__(self) -> str:
        return f'ID: {self.id} Title: {self.title} Status: {self.status} Project id: {self.project_id}'

    def __repr__(self):
        return str(self)

    def has_expected_status(self, expected_status: TaskStatus) -> bool:
        return self.status == expected_status

    def to_dict(self) -> dict[str, int | str | Decimal]:
        return {
            'id': self.id,
            'title': self.title,
            'status': self.status.name,
            'project_id': self.project_id,
        }


class CommentEntity(sa.Model):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    # TODO  zrobic conetnt jako unique.
    content: Mapped[str] = mapped_column(sa.String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'))
    task_id: Mapped[int] = mapped_column(sa.ForeignKey('tasks.id'))

    def has_expected_content(self, expected_content: str) -> bool:
        return self.content == expected_content

    def update_content(self, new_content: str) -> None:
        self.content = new_content

    def to_dict(self) -> dict[str, int | str | Decimal]:
        return {
            'id': self.id,
            'content': self.content,
            'creation data': str(self.created_at),
            'user_id': self.user_id,
            'task_id': self.task_id,
        }


class TaskHistoryEntity(sa.Model):
    __tablename__ = 'task_histories'

    id: Mapped[int] = mapped_column(primary_key=True)
    description_change: Mapped[str] = mapped_column(sa.String(30), nullable=False)
    task_id: Mapped[int] = mapped_column(sa.ForeignKey('tasks.id'))
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('users.id'))
