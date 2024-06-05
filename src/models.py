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
                            Session,
                            sessionmaker
                            )


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)

    projects: Mapped[list['Project']] = relationship('Project', back_populates='user')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='user')
    task_histories: Mapped[list['TaskHistory']] = relationship('TaskHistory', back_populates='user')


class Project(Base):
    __tablename__ = 'projects'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship('User', back_populates='projects')
    tasks: Mapped[list['Task']] = relationship('Task', back_populates='project')


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(30), nullable=False)
    project_id: Mapped[int] = mapped_column(ForeignKey('projects.id'))

    project: Mapped[Project] = relationship('Project', back_populates='tasks')
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='task')
    task_histories: Mapped[list['TaskHistory']] = relationship('TaskHistory', back_populates='task')


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(30), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))

    user: Mapped[User] = relationship('User', back_populates='comments')
    task: Mapped[User] = relationship('Task', back_populates='comments')


class TaskHistory(Base):
    __tablename__ = 'task_histories'

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    task: Mapped[Task] = relationship('Task', back_populates='task_histories')
    user: Mapped[User] = relationship('User', back_populates='task_histories')
