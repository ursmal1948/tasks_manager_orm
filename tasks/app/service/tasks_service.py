from app.db.repository import TaskRepository
from dataclasses import dataclass
from app.db.entity import TaskEntity, TaskStatus, ProjectEntity, UserEntity
from app.mail.configuration import MailSender


@dataclass
class TasksService:
    task_repository: TaskRepository

    # add todo zrobic metode dodajaca
    def get_by_id(self, task_id: int) -> TaskEntity | None:
        return self.task_repository.find_by_id(task_id)

    def get_by_title(self, title: str) -> TaskEntity:
        return self.task_repository.find_by_title(title)

    # def get_task_user_by_id(self, task_id: int) -> UserEntity:

    # def change_status(self, task_id: int, new_status: TaskStatus) -> None:
    #     task = self.task_repository.find_by_id(task_id)
    #     if task:
    #         # czy robic nowy task, czy podmieniac tylko status
    #         task.status = new_status
    #         self.task_repository.save_or_update(task)
    #         user_email = self.task_repository.find_project_id_by_task_id(task_id)
    #
    #         MailSender.send(user_email, f'Task status change', f'<h1>New status of task:{new_status}</h1>')

    def delete_task(self, task_id: int) -> None:
        task = self.task_repository.find_by_id(task_id)
        if task:
            self.task_repository.delete_by_id(task.id)

    def get_task_project(self, task_id: int) -> ProjectEntity:
        task = self.task_repository.find_by_id(task_id)
        if task:
            return self.task_repository.find_task_project(task.id)

    def get_tasks_by_status(self, task_status: TaskStatus) -> list[TaskEntity]:
        return self.task_repository.find_tasks_by_status(task_status)
