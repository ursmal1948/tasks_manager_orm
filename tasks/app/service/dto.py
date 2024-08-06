from typing import Self
from dataclasses import dataclass
from app.db.entity import TaskStatus


@dataclass
class CreateProjectDto:
    name: str
    description: str
    user_id: int

    @classmethod
    def from_dict(cls, data: dict[str, str | int]) -> Self:
        return cls(
            name=data['name'],
            description=data['description'],
            user_id=data['user_id']
        )

    def to_dict(self) -> dict[str, str | int]:
        return {
            "name": self.name,
            "description": self.description,
            "user_id": self.user_id
        }


@dataclass
class CreateUserWithProjectDto:
    username: str
    email: str
    password: str
    project_name: str
    project_description: str

    def to_dict(self) -> dict[str, str]:
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "project_name": self.project_name,
            "project_description": self.project_description,
        }

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        return cls(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            project_name=data["project_name"],
            project_description=data["project_description"]
        )


@dataclass
class CreateProjectWithTaskDto:
    project_name: str
    project_description: str
    user_id: int
    task_title: str
    task_status: TaskStatus

    def to_dict(self) -> dict[str, str | int]:
        return {
            "project_name": self.project_name,
            "project_description": self.project_description,
            "user_id": self.user_id,
            "task_title": self.task_title,
            "task_status": self.task_status
        }

    @classmethod
    def from_dict(cls, data: dict[str, str | int]) -> Self:
        return cls(
            project_name=data['project_name'],
            project_description=data['project_description'],
            user_id=data['user_id'],
            task_title=data['task_title'],
            task_status=TaskStatus[data.get('task_status', 'NEW')].name
        )
