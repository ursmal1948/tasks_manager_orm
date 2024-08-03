from flask import Blueprint, jsonify, Response, request
from jsonschema import validate

from app.service.configuration import (users_service,
                                       tasks_service,
                                       projects_service,
                                       projects_with_tasks_service,
                                       users_with_projects_service
                                       )

from app.routes.schemas import user_id_and_description_schema

projects_blueprint = Blueprint('projects', __name__, url_prefix='/projects')


@projects_blueprint.route('', methods=['GET'])
def get_projects_for_user():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'message': 'user_id is required'}), 400
    user_projects = users_service.get_users_projects(user_id)
    return jsonify({'projects': [p.to_dict() for p in user_projects]}), 200


@projects_blueprint.route('', methods=['GET'])
def get_all_projects() -> Response:
    return jsonify({'projects': [p.to_dict() for p in projects_service.get_all()]}), 200


@projects_blueprint.route('/<string:project_name>', methods=['POST'])
def add_project(project_name: str):
    request_data = request.json
    validate(instance=request_data, schema=user_id_and_description_schema)

    user_id = request_data['user_id']
    description = request_data['description']

    users_with_projects_service.add_project_to_user(
        project_name=project_name,
        project_description=description,
        user_id=user_id
    )
    return jsonify({'message': 'Project added successfully'}), 201


@projects_blueprint.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id: int):
    projects_service.delete_project(project_id=project_id)
    return jsonify({'message': 'project deleted'}), 200


@projects_blueprint.route('/', methods=['DELETE'])
def delete_all_projects():
    projects_service.delete_all()
    return jsonify({'message': 'projects deleted'}), 200


@projects_blueprint.route('/<int:project_id>/tasks', methods=['GET'])
def get_project_tasks(project_id: int) -> Response:
    tasks = projects_service.get_project_tasks(project_id=project_id)
    return jsonify({'tasks': [t.to_dict() for t in tasks]}), 200


@projects_blueprint.route('/', methods=['DELETE'])
def delete_user_projects():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'message': 'user_id is required'}), 400
    users_with_projects_service.delete_user_projects(user_id=user_id)
    return jsonify({'message': 'projects deleted'}), 200
