from app.persistence.repositories.models import TaskHistoryRepository
from unnecessary.persistence.models import TaskHistory


class TaskHistoryService:
    task_history_repo: TaskHistoryRepository

    def add_task_change(self, description_change: str, task_id: int, user_id: int):
        history = TaskHistory(description_change=description_change, task_id=task_id, user_id=user_id)
        self.task_history_repo.save_or_update(history)

    # TODO zapisywanie historii zmian w zadaniach.
    ## modyfikuje istneijacy juz obiekt i aktualizuje description change. Czy podejscie z
    ## tworzeniem nowego rekordu.
    def change_description(self, task_history_id: int, new_description: str) -> str:
        task_history = self.task_history_repo.find_by_id(task_history_id)
        if task_history:
            self.task_history_repo.save_or_update(
                TaskHistory(
                    id=task_history.id,
                    description_change=new_description,
                    task_id=task_history.task_id,
                    user_id=task_history.user_id
                )
            )
            return new_description
