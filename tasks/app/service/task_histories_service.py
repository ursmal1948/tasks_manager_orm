from dataclasses import dataclass
from app.db.entity import TaskHistoryEntity
from app.db.repository import (
    ProjectRepository,
    TaskRepository,
    UserRepository,
    TaskHistoryRepository,
)


@dataclass
class TaskHistoriesService:
    task_repository: TaskRepository
    user_repository: UserRepository
    task_history_repository: TaskHistoryRepository

    def add_task_history(
            self, task_id: int, user_id: int, description_change: str) \
            -> None:
        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError(f'Task with id {task_id} not found')
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f'User with id {user_id} not found')

        task_history = TaskHistoryEntity(
            task_id=task_id,
            user_id=user_id,
            description_change=description_change,
        )
        self.task_history_repository.save_or_update(task_history)

    def delete_task_history_by_id(self, task_history_id: int) -> None:
        task_history = self.task_history_repository.find_by_id(task_history_id)
        if not task_history:
            raise ValueError(f'Task history with id {task_history_id} not found')
        self.task_history_repository.delete_by_id(task_history_id)

    def get_task_histories_for_task(self, task_id: int) -> list[TaskHistoryEntity]:
        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError(f'Task {task_id} not found')
        return self.task_repository.find_task_histories_for_task(task_id)

    def delete_all_task_histories_for_task(self, task_id: int) -> None:
        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError(f'Task with id {task_id} not found')
        task_histories = self.task_repository.find_task_histories_for_task(task_id)
        if not task_histories:
            raise ValueError(f'No task histories for task id {task_id}')
        [self.task_history_repository.delete_by_id(task_history.id) for task_history in task_histories]
