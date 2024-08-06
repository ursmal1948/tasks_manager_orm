from dataclasses import dataclass
import logging
from app.db.entity import TaskEntity, TaskStatus, ProjectEntity
from app.db.repository import ProjectRepository, TaskRepository, UserRepository
from app.mail.configuration import MailSender
from app.service.dto import CreateProjectWithTaskDto

logging.basicConfig(level=logging.INFO)


@dataclass
class ProjectsWithTasksService:
    project_repository: ProjectRepository
    task_repository: TaskRepository
    user_repository: UserRepository

    def add_task_to_project(self, task_title: str, task_status: str, project_id: int) -> None:
        project = self.project_repository.find_by_id(project_id)
        if not project:
            raise ValueError(f'Project with id {project_id} does not exist')
        task = TaskEntity(
            title=task_title,
            status=task_status,
            project_id=project_id
        )
        self.task_repository.save_or_update(task)

    def add_project_with_task(self, create_project_with_task_dto: CreateProjectWithTaskDto):
        project_name = create_project_with_task_dto.project_name
        user_id = create_project_with_task_dto.user_id
        if self.project_repository.find_by_name(project_name):
            raise ValueError(f'Project with name {project_name} already exists')
        if not self.user_repository.find_by_id(user_id):
            raise ValueError(f'User with id {user_id} does not exist')

        project = ProjectEntity(
            name=project_name,
            description=create_project_with_task_dto.project_description,
            user_id=user_id
        )
        self.project_repository.save_or_update(project)
        added_project = self.project_repository.find_last_added_project()
        task = TaskEntity(
            title=create_project_with_task_dto.task_title,
            status=create_project_with_task_dto.task_status,
            project_id=added_project.id
        )
        self.task_repository.save_or_update(task)

    def delete_task_from_project(self, project_id: int) -> None:
        project = self.project_repository.find_by_id(project_id)
        if project:
            self.task_repository.delete_by_id(project_id)

    def change_task_status(self, task_id: int, new_status: TaskStatus) -> None:

        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError(f'Task with id {task_id} does not exist')
        task.set_status(new_status)
        self.task_repository.save_or_update(task)
        project_id = self.task_repository.find_project_id_by_task_id(task_id)
        user_id = self.project_repository.find_user_id_by_project_id(project_id)
        user_email = self.user_repository.find_email_by_id(user_id)

        MailSender.send(user_email, 'Task status has been changed', f'<h1>New status: {new_status.name}</h1>')
