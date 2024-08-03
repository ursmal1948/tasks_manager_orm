from flask import Blueprint, jsonify, Response, request
from jsonschema import validate
import logging
from app.service.configuration import (
    tasks_service,
    projects_service,
    projects_with_tasks_service
)
from app.db.entity import TaskStatus
from app.routes.schemas import status_and_project_id_schema, status_schema

logging.basicConfig(level=logging.INFO)
tasks_blueprint = Blueprint('tasks', __name__, url_prefix='/tasks')


@tasks_blueprint.route('/<int:task_id>', methods=['GET'])
def get_task(task_id: int) -> Response:
    task = tasks_service.get_by_id(task_id)
    return {'task': task.to_dict()}, 200


@tasks_blueprint.route('/<string:title>', methods=['POST'])
def add_task(title: str) -> Response:
    json_body = request.json
    validate(instance=json_body, schema=status_and_project_id_schema)

    status = TaskStatus[json_body.get('status', 'NEW')]
    project_id = json_body['project_id']

    projects_with_tasks_service.add_task_to_project(title, status, project_id)
    return jsonify({'message': 'task added'}), 200


@tasks_blueprint.route('/status/<int:task_id>', methods=['PUT'])
def update_task(task_id: int) -> Response:
    json_body = request.json
    validate(instance=json_body, schema=status_schema)
    status = TaskStatus[json_body['status']]
    projects_with_tasks_service.change_task_status(task_id, status)
    return jsonify({'message': 'task updated', 'status': status.name}), 200


@tasks_blueprint.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int) -> Response:
    tasks_service.delete_task(task_id)
    return jsonify({'message': 'task deleted'}), 200


@tasks_blueprint.route('/', methods=['GET'])
def fetch_tasks_by_status() -> Response:
    status_data = request.args.get('status')
    if status_data not in [
        TaskStatus.NEW.name,
        TaskStatus.IN_PROGRESS.name,
        TaskStatus.COMPLETED.name
    ]:
        return jsonify({'message': 'invalid status'}), 400
    status = TaskStatus[status_data]
    tasks = tasks_service.get_tasks_by_status(status)
    return {'tasks': [task.to_dict() for task in tasks] if tasks else []}, 200
