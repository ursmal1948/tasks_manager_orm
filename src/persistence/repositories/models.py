from src.persistence.repositories.orm import CrudRepositoryORM
from src.persistence.models import User, Project, Task, TaskHistory, TaskStatus

from sqlalchemy import select


class UserRepository(CrudRepositoryORM):
    def __init__(self, engine) -> None:
        super().__init__(engine, User)

    def find_by_name(self, name: str) -> User:
        with self._create_session() as session:
            stmt = select(User).filter_by(name=name)
            return session.execute(stmt).scalars().first()

    def find_all_projects_for_user(self, user_id: int) -> list[Project]:
        with self._create_session() as session:
            stmt = select(User).filter_by(id=user_id)
            user = session.execute(stmt).scalars().first()
            if user:
                print(user.name)
                return user.projects


class ProjectRepository(CrudRepositoryORM):
    def __init__(self, engine) -> None:
        super().__init__(engine, Project)

    def find_all_tasks_for_project(self, project_id: int) -> list[Task]:
        with self._create_session() as session:
            stmt = select(Project).filter_by(id=project_id)
            item = session.execute(stmt).scalars().first()
            if item:
                return item.tasks


class TaskRepository(CrudRepositoryORM):
    def __init__(self, engine) -> None:
        super().__init__(engine, Task)

    def find_tasks_by_status(self, task_status: TaskStatus) -> list[Task]:
        with self._create_session() as session:
            stmt = select(Task).filter_by(status=task_status)
            return session.execute(stmt).scalars().all()


class TaskHistoryRepository(CrudRepositoryORM):
    def __init__(self, engine) -> None:
        super().__init__(engine, TaskHistory)
