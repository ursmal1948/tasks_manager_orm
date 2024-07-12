from app.db.repository import UserRepository, ProjectRepository
from dataclasses import dataclass
from app.db.entity import ProjectEntity, TaskEntity


@dataclass
class ProjectsService:
    project_repository: ProjectRepository

    def get_all(self) -> list[ProjectEntity]:
        return self.project_repository.find_all()

    def get_by_id(self, project_id: int) -> ProjectEntity | None:
        return self.project_repository.find_by_id(project_id)

    def get_by_name(self, project_name: str) -> ProjectEntity | None:
        return self.project_repository.find_by_name(project_name)

    def delete_project(self, project_id: int) -> None:
        project = self.project_repository.find_by_id(project_id)
        if project:
            self.project_repository.delete_by_id(project.id)

    def change_project_description(self, project_id: int, description: str) -> None:
        project = self.project_repository.find_by_id(project_id)
        if project:
             # TODO ENKAPSULACJA
            project.description = description
            self.project_repository.save_or_update(project)

    def get_project_tasks(self, project_id: int) -> list[TaskEntity]:
        project = self.project_repository.find_by_id(project_id)
        if project:
            return self.project_repository.find_all_tasks_for_project(project.id)
