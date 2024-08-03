from flask import (
    jsonify,
    Response,
    Blueprint,
    request
)
from jsonschema import validate
import logging

from app.service.configuration import (
    users_service,
    projects_service,
    users_with_projects_service,
)
from app.routes.schemas import name_password_and_email_schema

logging.basicConfig(level=logging.INFO)

users_blueprint = Blueprint('users', __name__, url_prefix='/users')


@users_blueprint.route('/<string:username>/projects')
def get_projects_by_username(username: str) -> Response:
    user = users_service.get_by_name(username)
    projects = users_service.get_users_projects(user.id)
    return jsonify({'projects': [p.to_dict() for p in projects]}), 200


@users_blueprint.route('/<int:user_id>/projects')
def get_projects_by_id(user_id: str) -> Response:
    projects = users_service.get_users_projects(user_id)
    return jsonify({'projects': [p.to_dict() for p in projects] if projects else []}), 200


@users_blueprint.route('/<int:user_id>')
def get_user_by_id(user_id: int) -> Response:
    user = users_service.get_by_id(user_id)
    return {'user': user.to_dict()}, 200


@users_blueprint.route('<int:user_id>', methods=['PUT'])
def update_user_by_id(user_id: int) -> Response:
    json_body = request.json
    validate(instance=json_body, schema=name_password_and_email_schema)

    users_service.update_user(
        user_id=user_id,
        name=json_body['name'],
        password=json_body['password'],
        email=json_body['email']
    )
    return jsonify({'message': 'user updated'}), 200


@users_blueprint.route('<int:user_id>', methods=['DELETE'])
def delete_user_by_id(user_id: int) -> Response:
    users_service.delete_user(user_id)
    return jsonify({'message': 'user deleted successfully'}), 200


@users_blueprint.route('', methods=['DELETE'])
def delete_all_users() -> Response:
    users_service.delete_all_users()
    return jsonify({'message': 'all users deleted'}), 200
