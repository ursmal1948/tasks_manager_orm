from app.db.entity import UserEntity, ProjectEntity
from dataclasses import dataclass
from app.db.repository import UserRepository, ProjectRepository


@dataclass
class UsersService:
    user_repository: UserRepository

    def get_all(self) -> list[UserEntity]:
        return self.user_repository.find_all()

    def get_by_name(self, name: str) -> UserEntity | None:
        return self.user_repository.find_by_name(name)

    def get_by_email(self, email: str) -> UserEntity | None:
        return self.user_repository.find_by_email(email)

    def get_by_id(self, user_id: int) -> UserEntity | None:
        return self.user_repository.find_by_id(user_id)

    def add_user(self, name: str, email: str, password: str) -> None:
        self.user_repository.save_or_update(
            UserEntity(
                name=name,
                email=email,
                password=password
            )
        )

    # todo , moze tylko update ser mail. i bym przekazywala user_id, i new_email.
    def update_user(self, user_id: int, name: str, email: str, password: str) -> None:
        self.user_repository.save_or_update(
            UserEntity(
                id=user_id,
                name=name,
                email=email,
                password=password
            )
        )

    def delete_user(self, id_: int) -> None:
        self.user_repository.delete_by_id(id_)

    # todo czy np blad ValueError jak nie znajde takiego usera.
    #   bo tak naprawde to powtarzam logike.

    def get_users_projects(self, user_id: int) -> list[ProjectEntity]:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError(f'User {user_id} not found')
        if self.user_repository.find_by_id(user_id):
            return self.user_repository.find_all_projects_for_user(user_id)
