from dataclasses import dataclass
from app.db.repository import TaskRepository
from app.db.entity import (
    TaskEntity,
    TaskStatus,
    ProjectEntity,
    UserEntity
)


@dataclass
class TasksService:
    task_repository: TaskRepository

    def get_by_id(self, task_id: int) -> TaskEntity | None:
        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError(f'Task with id {task_id} not found')
        return task

    def delete_task(self, task_id: int) -> None:
        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError(f'Task with id {task_id} not found')
        self.task_repository.delete_by_id(task_id)

    def get_tasks_by_status(self, task_status: TaskStatus) -> list[TaskEntity]:
        return self.task_repository.find_tasks_by_status(task_status)
