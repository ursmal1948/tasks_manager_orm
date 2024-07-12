# from sqlalchemy import create_engine
# from app.service.user_with_project import UsersService, ProjectService
# from app.persistence.repositories.models import UserRepository, ProjectRepository, TaskRepository
# from app.persistence.configuration import engine
#
#
# def main() -> None:
#     user_repo = UserRepository(engine)
#     project_repo = ProjectRepository(engine)
#     task_repo = TaskRepository(engine)
#     user_service = UsersService(user_repo)
#     project_service = ProjectService(project_repo)
#     user_service.create_user(name='C', email='c@gmail.com', password='PAS3')
#     # user_and_project_service = UserAndProjectService(user_repo=user_repo, project_repo=project_repo)
#     # print(user_and_project_service.add_project_to_user(user_id=1, project_name='PA'))
#
#     # task_and_project_service = ProjectAndTaskService(project_repo=project_repo, task_repo=task_repo)
#     # print(task_and_project_service.add_task_to_project(project_id=1, task_title='TB'))
#     # task = task_repo.find_by_id(2)
#     # print(task)
#
#
# if __name__ == '__main__':
#     main()
