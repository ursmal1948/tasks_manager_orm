import enum
from datetime import datetime
from sqlalchemy import (
    ForeignKey,
    String,
    select,
    create_engine,
    text,
    DateTime
)
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            relationship,
                            sessionmaker
                            )
from enum import Enum


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(30), nullable=False)

    projects: Mapped[list['Project']] = relationship('Project', back_populates='user')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='user')
    task_histories: Mapped[list['TaskHistory']] = relationship('TaskHistory', back_populates='user')

    def __str__(self) -> str:
        return f'ID: {self.id} NAME: {self.name}'

    def __repr__(self):
        return str(self)


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    # description: Mapped[str] = mapped_column(String(30), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship('User', back_populates='projects')
    tasks: Mapped[list['Task']] = relationship('Task', back_populates='project')

    def __str__(self) -> str:
        return f'ID: {self.id} Project: {self.name}'

    def __repr__(self):
        return str(self)


class TaskStatus(Enum):
    NEW = 0
    IN_PROGRESS = 1
    COMPLETED = 2


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(default=TaskStatus.NEW)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))

    project: Mapped[Project] = relationship('Project', back_populates='tasks')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='task')
    task_histories: Mapped[list['TaskHistory']] = relationship('TaskHistory', back_populates='task')

    def __str__(self) -> str:
        return f'ID: {self.id} Task: {self.title} Staus: {self.status.name}'

    def __repr__(self):
        return str(self)


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))

    user: Mapped[User] = relationship('User', back_populates='comments')
    task: Mapped[User] = relationship('Task', back_populates='comments')

    def __str__(self) -> str:
        return f'ID: {self.id} Comment: {self.content}'

    def __repr__(self):
        return str(self)


class TaskHistory(Base):
    __tablename__ = 'task_histories'

    id: Mapped[int] = mapped_column(primary_key=True)
    description_change: Mapped[str] = mapped_column(String(30), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    task: Mapped[Task] = relationship('Task', back_populates='task_histories')
    user: Mapped[User] = relationship('User', back_populates='task_histories')

    def __str__(self) -> str:
        return f'ID: {self.id} Task History: {self.description_change}'

    def __repr__(self):
        return str(self)
#
#
# def main() -> None:
#     metadata = Base.metadata
#     metadata.create_all(engine)
#
#
# if __name__ == '__main__':
#     main()
