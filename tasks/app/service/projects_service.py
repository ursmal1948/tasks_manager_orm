from dataclasses import dataclass
from app.db.entity import ProjectEntity, TaskEntity
from app.db.repository import UserRepository, ProjectRepository


@dataclass
class ProjectsService:
    project_repository: ProjectRepository

    def get_all(self) -> list[ProjectEntity]:
        return self.project_repository.find_all()

    def delete_project(self, project_id: int) -> None:
        project = self.project_repository.find_by_id(project_id)
        if not project:
            raise ValueError(f'Project with id {project_id} not found')
        self.project_repository.delete_by_id(project.id)

    def delete_all(self) -> None:
        if not self.project_repository.find_all():
            raise ValueError('No projects to delete')
        self.project_repository.delete_all()

    def get_project_tasks(self, project_id: int) -> list[TaskEntity]:
        if not self.project_repository.find_by_id(project_id):
            raise ValueError(f'Project with id {project_id} not found')
        return self.project_repository.find_all_tasks_for_project(project_id)
