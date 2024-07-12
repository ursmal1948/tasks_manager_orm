from dataclasses import dataclass
from unnecessary.persistence.models import Task, TaskStatus
from app.persistence.repositories.models import ProjectRepository, TaskRepository


@dataclass
class TasksService:
    task_repo: TaskRepository

    def change_task_status(self, task_id: int, new_status: TaskStatus) -> Task:
        task = self.task_repo.find_by_id(task_id)
        if task:
            task_with_new_status = Task(
                id=task.id,
                title=task.title,
                status=new_status,
                project_id=task.project_id
            )
            self.task_repo.save_or_update(task_with_new_status)
            return task_with_new_status


@dataclass
class ProjectsWithTasksService:
    project_repo: ProjectRepository
    task_repo: TaskRepository

    def add_task_to_project(self, project_id: int, task_title: str) -> Task:
        project = self.project_repo.find_by_id(project_id)
        if project:
            task_to_add = Task(title=task_title, project_id=project.id)
            self.task_repo.save_or_update(task_to_add)
            return task_to_add
