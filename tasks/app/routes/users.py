from flask import (
    Flask,
    jsonify,
    request,
    Response,
    make_response,
    Blueprint,
    request
)
from flask_restful import Resource, reqparse

from app.service.configuration import users_service
import logging

users_blueprint = Blueprint('users', __name__, url_prefix='/users')

from sqlalchemy.sql.functions import user

logging.basicConfig(level=logging.INFO)
from app.service.configuration import (
    users_service,
    projects_service,
    users_with_projects_service
)


@users_blueprint.route('/<string:name>/projects')
def get_projects(name: str) -> Response:
    user = users_service.get_by_name(name)
    if user:
        projects = users_service.get_users_projects(user.id)
        return jsonify({'projects': [project.to_dict() for project in projects]})
    return jsonify({'message': 'User not found'}), 404


# TODO resource UserIDResource users/id/<int:user_id> z metodami
#   get,update i delete (post tez, bede miala id usera ostatnio wstawionego do bazy?)
#    W jaka konwencje isc?Resource czy funkcje ponizej.
#   i forma dokumentacji czy w w pathie zawrzec tez nazwe metody http


# users/get/<int:user_id>
@users_blueprint.route('/<int:user_id>')
def get_user_by_id(user_id: int) -> Response:
    user = users_service.get_by_id(user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'message': 'User not found'}), 404


# users/update/<int:user_id>

@users_blueprint.route('<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id: int) -> Response:
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help='Name of user', required=True)
    parser.add_argument('password', type=str, help='Password of user', required=True)
    parser.add_argument('email', type=str, help='Email of user', required=True)

    request_data = parser.parse_args()
    user = users_service.get_by_id(user_id)
    if user:
        users_service.update_user(
            user_id=user.id,
            name=request_data['name'],
            password=request_data['password'],
            email=request_data['email']
        )
        return jsonify({'message': 'User updated seccessfully'}), 200
    return jsonify({'message': 'User not found'}), 404


@users_blueprint.route('<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id: int) -> Response:
    user_to_delete = users_service.get_by_id(user_id)
    if user_to_delete:
        users_service.delete_user(user_to_delete.id)
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'message': 'User not found'}), 404


@users_blueprint.route('', methods=['GET'])
def get_users() -> Response:
    users = users_service.get_all()
    if users:
        return jsonify({'users': [user.to_dict() for user in users]})
    return jsonify({'message': 'Users not found'}), 404
