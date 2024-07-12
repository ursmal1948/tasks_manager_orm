from app.db.repository import CommentRepository, UserRepository, TaskRepository
from dataclasses import dataclass
from app.db.entity import CommentEntity
import datetime

import logging

logging.basicConfig(level=logging.INFO)


@dataclass
class CommentsService:
    comment_repository: CommentRepository
    user_repository: UserRepository
    task_repository: TaskRepository

    def add_comment(self, content: str, creation_data: datetime, user_id: int, task_id: int) -> None:
        if not self.user_repository.find_by_id(user_id):
            raise ValueError(f'User {user_id} does not exist')
        if not self.task_repository.find_by_id(task_id):
            raise ValueError(f'Task {task_id} does not exist')

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
            raise ValueError(f'Comment {comment_id} does not exist')
        comment.update_content(new_content)
        logging.info(f'COMMENT {comment_id} updated')
        self.comment_repository.save_or_update(comment)

    def get_by_content(self, content: str) -> CommentEntity:
        return self.comment_repository.find_by_content(content)

    def get_by_id(self, comment_id: int) -> CommentEntity:
        return self.comment_repository.find_by_id(comment_id)

    def get_all(self) -> list[CommentEntity]:
        return self.comment_repository.find_all()

    def delete_comment(self, comment_id: int) -> None:
        self.comment_repository.delete_by_id(comment_id)
