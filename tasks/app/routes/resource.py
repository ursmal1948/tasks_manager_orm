from flask_restful import Resource
from flask import Response, jsonify, request
import logging
from jsonschema import validate

from app.service.configuration import (
    users_service,
    projects_service,
    users_with_projects_service,
    comments_service,
    task_histories_service
)
from app.routes.schemas import (
    email_and_password_schema,
    name_and_password_schema,
    user_id_task_id_and_creation_data_schema,
    user_id_and_description_schema,
    user_with_project_schema,
    validate_email,
    validate_name
)
import datetime

logging.basicConfig(level=logging.INFO)


class UserNameResource(Resource):

    def get(self, name: str) -> Response:
        user = users_service.get_by_name(name)
        return {'user': user.to_dict()}, 201

    def post(self, name: str) -> Response:
        if not validate_name(name):
            return {'message': 'invalid name'}, 400
        json_body = request.json
        validate(instance=json_body, schema=email_and_password_schema)

        users_service.add_user(
            name=name,
            email=json_body['email'],
            password=json_body['password']
        )
        added_user = users_service.get_last_added_user()
        return {'user': added_user.to_dict()}, 201

    def delete(self, name: str) -> Response:
        user = users_service.get_by_name(name)
        users_service.delete_user(user.id)
        return {'message': 'user deleted'}, 200


class UserEmailResource(Resource):

    def get(self, email: str) -> Response:
        user = users_service.get_by_email(email)
        return {'user': user.to_dict()}, 200

    def post(self, email: str) -> Response:
        if not validate_email(email):
            return {'message': 'invalid email'}, 400

        json_body = request.json
        validate(instance=json_body, schema=name_and_password_schema)

        users_service.add_user(
            name=json_body['name'],
            email=email,
            password=json_body['password']
        )
        added_user = users_service.get_last_added_user()
        return {'user': added_user.to_dict()}, 201

    def delete(self, email: str) -> Response:
        user = users_service.get_by_email(email)
        users_service.delete_user(user.id)
        return jsonify({'message': 'user deleted'}), 200


class UsersListResource(Resource):
    def get(self) -> Response:
        users = users_service.get_all()
        return {'users': [user.to_dict() for user in users]}, 200


class CommentContentResource(Resource):

    def get(self, content: str) -> Response:
        comment = comments_service.get_by_content(content)
        return {'comment': comment.to_dict()}, 200

    def post(self, content: str) -> Response:
        json_body = request.json
        validate(instance=json_body, schema=user_id_task_id_and_creation_data_schema)
        user_id = json_body['user_id']
        task_id = json_body['task_id']
        creation_date = json_body.get('creation_date', datetime.datetime.now())

        comments_service.add_comment(
            content=content,
            creation_data=creation_date,
            user_id=user_id,
            task_id=task_id
        )
        return {'message': 'comment added'}, 200

    def delete(self, content: str) -> Response:
        comment = comments_service.get_by_content(content)
        comments_service.delete_comment(comment.id)
        return {'message': 'comment deleted'}, 200


class CommentIdResource(Resource):
    def get(self, comment_id: int) -> Response:
        comment = comments_service.get_by_id(comment_id)
        return {'comment': comment.to_dict()}, 200

    def delete(self, comment_id: int) -> Response:
        comments_service.delete_comment(comment_id)
        return {'message': 'comment deleted'}


class CommentsListResource(Resource):
    def get(self) -> Response:
        comments = comments_service.get_all()
        return {'comments': [comment.to_dict() for comment in comments]}, 200


class TaskHistoryTaskIdResource(Resource):
    def get(self, task_id: int) -> Response:
        histories = task_histories_service.get_task_histories_for_task(task_id)
        return jsonify({'task_histories': [history.to_dict() for history in histories]})

    def post(self, task_id: int) -> Response:
        json_body = request.json
        validate(instance=json_body, schema=user_id_and_description_schema)
        user_id = json_body['user_id']
        description_change = json_body['description']

        task_histories_service.add_task_history(
            task_id=task_id,
            user_id=user_id,
            description_change=description_change
        )
        return {'message': 'task history added', 'task_id': task_id}, 200

    def delete(self, task_id: int) -> Response:
        task_histories_service.delete_all_task_histories_for_task(task_id)
        return {'message': 'task histories deleted', 'task_id': task_id}, 200


class UserWithProjectResource(Resource):
    def post(self) -> Response:
        json_body = request.json
        validate(instance=json_body, schema=user_with_project_schema)
        username = json_body['username']
        email = json_body['email']
        password = json_body['password']
        project_name = json_body['project_name']
        project_description = json_body['project_description']

        users_with_projects_service.add_user_with_project(
            username=username,
            email=email,
            password=password,
            project_name=project_name,
            project_description=project_description
        )
        return {'message': 'user and project added'}, 201
