from dataclasses import dataclass
from src.persistence.repositories.models import UserRepository, ProjectRepository
from src.persistence.models import User, Project, Task


@dataclass
class UsersService:
    user_repo: UserRepository

    def create_user(self, name: str, email: str, password: str) -> User:
        user = User(name=name, email=email, password=password)
        self.user_repo.save_or_update(user)
        return user

    def change_user_name(self, user_id: int, new_name: str) -> str:
        user = self.user_repo.find_by_id(user_id)
        if user:
            self.user_repo.save_or_update(
                User(
                    id=user_id,
                    name=new_name,
                    email=user.email,
                    password=user.password
                )
            )
            return new_name

    def get_user(self, user_id: int) -> User | None:
        return self.user_repo.find_by_id(user_id)

    def delete_user(self, user_id: int) -> None:
        self.user_repo.delete_by_id(user_id)

    def get_user_projects(self, user_id: int) -> list[Project]:
        return self.user_repo.find_all_projects_for_user(user_id=user_id)


@dataclass
class ProjectService:
    project_repo: ProjectRepository

    def change_project_name(self, project_id: int, new_project_name: str) -> str:
        project = self.project_repo.find_by_id(project_id)
        if project:
            self.project_repo.save_or_update(Project(
                id=project.id,
                name=new_project_name,
                user_id=project.user_id
            ))
            return new_project_name

    def get_project_tasks(self, project_id: int) -> list[Task]:
        tasks = self.project_repo.find_all_tasks_for_project(project_id=project_id)
        return tasks


@dataclass
class UsersWithProjectsService:
    user_repo: UserRepository
    project_repo: ProjectRepository

    def add_user_with_project(self, user_name: str, user_email: str, user_password: str, project_name: str):
        self.user_repo.save_or_update(User(name=user_name, email=user_email, password=user_password))
        user = self.user_repo.find_by_name(user_name)
        project = Project(name=project_name, user_id=user.id)
        self.project_repo.save_or_update(project)
        return user.id, project_name

    def add_project_to_user(self, user_id: int, project_name: str) -> Project:
        user = self.user_repo.find_by_id(user_id)
        if user:
            project = Project(name=project_name, user_id=user.id)
            self.project_repo.save_or_update(project)
            return project

    # def get_projects_with_desired_status_
