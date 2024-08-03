from dataclasses import dataclass
import datetime
import logging

from app.db.entity import CommentEntity
from app.db.repository import (
    CommentRepository,
    UserRepository,
    TaskRepository
)

logging.basicConfig(level=logging.INFO)


@dataclass
class CommentsService:
    comment_repository: CommentRepository
    user_repository: UserRepository
    task_repository: TaskRepository

    def add_comment(self, content: str, creation_data: datetime, user_id: int, task_id: int) -> None:
        if not self.user_repository.find_by_id(user_id):
            raise ValueError(f'User with id {user_id} not found')
        if not self.task_repository.find_by_id(task_id):
            raise ValueError(f'Task with id {task_id} not found')
        if self.comment_repository.find_by_content(content):
            raise ValueError(f'Content {content} already exists')
        self.comment_repository.save_or_update(
            CommentEntity(
                content=content,
                created_at=creation_data,
                user_id=user_id,
                task_id=task_id,
            )
        )

    def change_comment_content(self, comment_id: int, new_content: str) -> None:
        comment = self.comment_repository.find_by_id(comment_id)
        if not comment:
            raise ValueError(f'Comment with id {comment_id} not found')
        if comment.has_expected_content(new_content):
            raise ValueError('Comment already has expected content')
        comment.update_content(new_content)
        self.comment_repository.save_or_update(comment)

    def get_by_content(self, content: str) -> CommentEntity:
        comment = self.comment_repository.find_by_content(content)
        if not comment:
            raise ValueError(f'Comment with content {content} not found')
        return self.comment_repository.find_by_content(content)

    def get_by_id(self, comment_id: int) -> CommentEntity:
        comment = self.comment_repository.find_by_id(comment_id)
        if not comment:
            raise ValueError(f'Comment with id {comment_id} not found')
        return comment

    def get_all(self) -> list[CommentEntity]:
        return self.comment_repository.find_all()

    def delete_comment(self, comment_id: int) -> None:
        comment = self.comment_repository.find_by_id(comment_id)
        if not comment:
            raise ValueError(f'Comment with id {comment_id} not found')
        self.comment_repository.delete_by_id(comment_id)
