from dataclasses import dataclass
from app.db.entity import UserEntity, ProjectEntity
from app.db.repository import UserRepository, ProjectRepository
from app.service.dto import CreateUserWithProjectDto, CreateProjectDto

import logging

logging.basicConfig(level=logging.INFO)


@dataclass
class UsersWithProjectsService:
    user_repository: UserRepository
    project_repository: ProjectRepository

    def add_user_with_project(self, create_user_with_project_dto: CreateUserWithProjectDto) -> None:

        username = create_user_with_project_dto.username
        email = create_user_with_project_dto.email
        project_name = create_user_with_project_dto.project_name

        if self.user_repository.find_by_name(username):
            raise ValueError(f'User with name {username} already exists')
        if self.user_repository.find_by_email(email):
            raise ValueError(f'User with email {email} already exists')
        if self.project_repository.find_by_name(project_name):
            raise ValueError(f'Project with name {project_name} already exists')

        self.user_repository.save_or_update(UserEntity(
            name=username,
            email=email,
            password=create_user_with_project_dto.password)
        )

        added_user = self.user_repository.find_last_added_user()
        user_project = ProjectEntity(
            name=project_name,
            description=create_user_with_project_dto.project_description,
            user_id=added_user.id)
        self.project_repository.save_or_update(user_project)

    def add_project_to_user(self, create_project_dto: CreateProjectDto) -> None:
        user_id = create_project_dto.user_id
        user = self.user_repository.find_by_id(user_id)
        project_name = create_project_dto.name
        if not user:
            raise ValueError(f'User with id {user_id} does not exist')

        if self.project_repository.find_by_name(project_name):
            raise ValueError(f'Project with name {project_name} already exists')

        project = ProjectEntity(
            name=project_name,
            description=create_project_dto.description,
            user_id=user_id)

        self.project_repository.save_or_update(project)

    def delete_user_projects(self, user_id: int) -> None:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f'User with id {user_id} does not exist')
        user_projects = self.user_repository.find_all_projects_for_user(user.id)
        if not user_projects:
            raise ValueError(f'User with id {user_id} has no projects')
        [self.project_repository.delete_by_id(user_project.id) for user_project in user_projects]
