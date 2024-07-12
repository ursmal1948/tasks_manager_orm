from dataclasses import dataclass
from app.db.repository import UserRepository, ProjectRepository
from app.db.entity import UserEntity, ProjectEntity


@dataclass
class UsersWithProjectsService:
    user_repo: UserRepository
    project_repo: ProjectRepository

    def add_user_with_project(self,
                              user_name: str,
                              user_email: str,
                              user_password: str,
                              project_name: str,
                              project_description: str) -> None:
        self.user_repo.save_or_update(UserEntity(name=user_name, email=user_email, password=user_password))
        user = self.user_repo.find_by_name(user_name)
        user_project = ProjectEntity(name=project_name, description=project_description, user_id=user.id)
        self.project_repo.save_or_update(user_project)

    def add_project_to_user(self, project_name: str, project_description: str, user_id: int) -> None:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError(f'User with id {user_id} does not exist')
        project = ProjectEntity(name=project_name, description=project_description, user_id=user.id)
        self.project_repo.save_or_update(project)

    def delete_user_projects(self, user_id: int) -> None:
        user = self.user_repo.find_by_id(user_id)
        user_projects = self.user_repo.find_all_projects_for_user(user.id)
        [self.project_repo.delete_by_id(user_project.id) for user_project in user_projects]
