from flask_restful import Resource, reqparse
from flask import Response, jsonify, make_response, current_app
import logging
from flask_json_schema import JsonSchema, JsonValidationError

from app.db.entity import UserEntity, ProjectEntity, CommentEntity
from app.service.configuration import (
    users_service,
    projects_service,
    users_with_projects_service,
    comments_service
)
import datetime

logging.basicConfig(level=logging.INFO)
from dataclasses import dataclass


# TODO STATYCZNE METODY.

class UserNameResource(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('email', type=str, required=True, help='email of user is required')
    parser.add_argument('password', type=str, required=True, help='Password of user is required')

    def get(name: str) -> Response:
        user = users_service.get_by_name(name)
        if user:
            return jsonify({'user': user.to_dict(), 'status': 201})
        return {'message': 'User not fouund'}, 404

    def post(self, name: str) -> Response:
        try:
            if users_service.get_by_name(name):
                return {'message': 'User already exists'}, 400
            request_data = UserNameResource.parser.parse_args()

            users_service.add_user(
                name=name,
                email=request_data['email'],
                password=request_data['password']
            )
            user = users_service.get_by_name(name)
            return {'user': user.to_dict()}, 201
        except Exception as e:
            logging.error(e)
            return {'message': 'Cannot create user'}, 500

    def delete(self, name: str) -> Response:
        user = users_service.get_by_name(name)
        if user:
            users_service.delete_user(user.id)
            return {'message': 'User deleted'}
        return {'user': 'User does not exist'}, 500


class UsersListResource(Resource):
    def get(self) -> Response:
        return {'users': [user.to_dict() for user in users_service.get_all()]}, 200


class UserEmailResource(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('name', type=str, required=True, help='email of user is required')
    parser.add_argument('password', type=str, required=True, help='Password of user is required')

    def get(self, email: str) -> Response:
        user = users_service.get_by_email(email)
        if user:
            return jsonify({'user': user.to_dict(), 'status': 201})
        return {'message': 'User not fouund'}, 404

    def post(self, email: str) -> Response:
        try:
            if users_service.get_by_email(email):
                return {'message': 'User already exists'}, 400
            request_data = UserEmailResource.parser.parse_args()

            users_service.add_user(
                name=request_data['name'],
                email=email,
                password=request_data['password']
            )
            user = users_service.get_by_email(email)
            return {'user': user.to_dict()}, 201
        except Exception as e:
            logging.error(e)
            return {'message': 'Cannot create user'}, 500

    def delete(self, email: str) -> Response:
        user = users_service.get_by_email(email)
        if user:
            users_service.delete_user(user.id)
            return {'message': 'User deleted'}
        return {'user': 'User does not exist'}, 500


class CommentContentResource(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('creation_data', type=datetime, help='Data creation of comment',
                        default=datetime.datetime.now())
    parser.add_argument('user_id', type=int, required=True, help='User id required')
    parser.add_argument('task_id', type=int, required=True, help='Task id required')

    def get(self, content: str) -> Response:
        comment = comments_service.get_by_content(content)
        if comment:
            return jsonify({'comment': comment.to_dict(), 'status': 201})
        return {'message': 'Comment not found'}, 404

    def post(self, content: str) -> Response:
        try:
            if comments_service.get_by_content(content):
                return {'message': 'Comment already exists'}, 400

            request_data = CommentContentResource.parser.parse_args()
            comments_service.add_comment(
                content=content,
                creation_data=request_data['creation_data'],
                user_id=request_data['user_id'],
                task_id=request_data['task_id']
            )
            return {'message': 'Comment created'}, 201
        except Exception as e:
            logging.error(e)
            return {'message': 'Cannot create comment'}, 500

    def delete(self, content: str) -> Response:
        comment = comments_service.get_by_content(content)
        if comment:
            comments_service.delete_comment(comment.id)
            return {'message': 'Comment deleted'}
        return {'message': 'Comment does not exist'}, 500


class CommentIdResource(Resource):
    def get(self, comment_id: int) -> Response:
        comment = comments_service.get_by_id(comment_id)
        if comment:
            return jsonify({'comment': comment.to_dict(), 'status': 201})
        return {'message': 'Comment not found'}, 404

    def delete(self, comment_id: int):
        comment = comments_service.get_by_id(comment_id)
        if comment:
            comments_service.delete_comment(comment.id)
            return {'message': 'Comment deleted'}
        return {'message': 'Comment does not exist'}, 500


class CommentsListResource(Resource):
    def get(self) -> Response:
        return [comment.to_dict() for comment in comments_service.get_all()], 200

    # def post(self, content: str) -> Response:
    #     comment=
# 2024-07-10T02:05:20.269914
