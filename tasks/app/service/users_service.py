from dataclasses import dataclass
from app.db.entity import UserEntity, ProjectEntity
from app.db.repository import UserRepository, ProjectRepository


@dataclass
class UsersService:
    user_repository: UserRepository

    def get_all(self) -> list[UserEntity]:
        return self.user_repository.find_all()

    def get_by_name(self, name: str) -> UserEntity:
        user = self.user_repository.find_by_name(name)
        if not user:
            raise ValueError(f'User with name {name} does not exist')
        return user

    def get_by_email(self, email: str) -> UserEntity | None:
        user = self.user_repository.find_by_email(email)
        if not user:
            raise ValueError(f'User with email {email} does not exist')
        return user

    def get_by_id(self, user_id: int) -> UserEntity | None:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f'User with id {user_id} does not exist')
        return user

    def add_user(self, name: str, email: str, password: str) -> None:
        if self.user_repository.find_by_name(name):
            raise ValueError(f'User with name {name} already exists')
        if self.user_repository.find_by_email(email):
            raise ValueError(f'User with email {email} already exists')
        self.user_repository.save_or_update(
            UserEntity(
                name=name,
                email=email,
                password=password
            )
        )

    def update_user(self, user_id: int, name: str, email: str, password: str) -> None:
        if not self.user_repository.find_by_id(user_id):
            raise ValueError(f'User with id {user_id} does not exist')
        self.user_repository.save_or_update(
            UserEntity(
                id=user_id,
                name=name,
                email=email,
                password=password
            )
        )

    def delete_user(self, user_id: int) -> None:
        user_to_delete = self.user_repository.find_by_id(user_id)
        if not user_to_delete:
            raise ValueError(f'User with id {user_id} does not exist')
        self.user_repository.delete_by_id(user_id)

    def get_last_added_user(self) -> UserEntity:
        last_added_user = self.user_repository.find_last_added_user()
        if not last_added_user:
            raise ValueError('No last added user')
        return last_added_user

    def get_users_projects(self, user_id: int) -> list[ProjectEntity]:
        if not self.user_repository.find_by_id(user_id):
            raise ValueError(f'User with id {user_id} does not exist')
        return self.user_repository.find_all_projects_for_user(user_id)

    def delete_all_users(self) -> None:
        if not self.user_repository.find_all():
            raise ValueError('No users to delete')
        self.user_repository.delete_all()
