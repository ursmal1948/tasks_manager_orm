from app.db.repository import (
    project_repository,
    user_repository,
    task_repository,
    comment_repository,
    task_history_repository
)
from app.service.users_service import UsersService
from app.service.projects_service import ProjectsService
from app.service.users_with_projects import UsersWithProjectsService
from app.service.projects_with_tasks_service import ProjectsWithTasksService
from app.service.tasks_service import TasksService
from app.service.comments_service import CommentsService
from app.service.task_histories_service import TaskHistoriesService

users_service = UsersService(user_repository)
projects_service = ProjectsService(project_repository)
users_with_projects_service = UsersWithProjectsService(user_repository, project_repository)
projects_with_tasks_service = ProjectsWithTasksService(project_repository, task_repository, user_repository)
tasks_service = TasksService(task_repository)
comments_service = CommentsService(comment_repository, user_repository, task_repository)
task_histories_service = TaskHistoriesService(task_repository, user_repository,task_history_repository)
