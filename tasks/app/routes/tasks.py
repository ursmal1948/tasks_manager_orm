from flask import Blueprint, jsonify, Response
from app.service.configuration import tasks_service, projects_service, projects_with_tasks_service
from flask_restful import reqparse, request
from flask_json_schema import JsonSchema, JsonValidationError
from app.db.entity import TaskStatus
import logging
# from app.routes.blueprints import tasks_blueprint
tasks_blueprint = Blueprint('tasks', __name__, url_prefix='/tasks')

logging.basicConfig(level=logging.INFO)


# todo forma dokumentowania. add, get delete itp /get/<int:task_id>

@tasks_blueprint.route('/<int:task_id>', methods=['GET'])
def get_task(task_id: int) -> Response:
    task = tasks_service.get_by_id(task_id)
    if task:
        return jsonify({'task': task.to_dict()}), 200
    return jsonify({'message': 'Task not found'}), 404


@tasks_blueprint.route('/<string:title>', methods=['POST'])
def add_task(title: str) -> Response:
    try:
        parser = reqparse.RequestParser()

        parser.add_argument('status', type=str, required=True, help='Task status')
        parser.add_argument('project_id', type=int, required=True, help='Project id')

        request_data = parser.parse_args()
        status = TaskStatus.from_str(request_data['status'])
        project_id = int(request_data['project_id'])

        projects_with_tasks_service.add_task_to_project(title, status, project_id)
        if tasks_service.get_by_title(title):
            return jsonify({'message': 'Task added successfully'}), 200
    except Exception as e:
        logging.info(e)
        return jsonify({'message': 'Cannot create task'}), 404


# update tych elementow. naazwa sciezki
# /task_status/<int:task_id> /update_task_status/<int:task_id>
# /project_id<int:task_id>
# /title/<int:task_id>
@tasks_blueprint.route('/task_status/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, required=True, help='New task status')
        task = tasks_service.get_by_id(task_id)
        if task:
            request_data = parser.parse_args()
            status = TaskStatus[request_data['status']]
            if task.has_expected_status(status):
                return jsonify({'message': 'Task already has the same status'}), 304
            projects_with_tasks_service.change_task_status(task.id, status)

            return jsonify({'message': 'Task updated successfully', 'status': task.status.name}), 200
        return jsonify({'message': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'message': 'Cannot update task'}), 404


@tasks_blueprint.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int) -> Response:
    task = tasks_service.get_by_id(task_id)
    if task:
        tasks_service.delete_task(task.id)
        return jsonify({'message': 'Task deleted successfully'}), 200
    return jsonify({'message': 'Task not found'}), 404


@tasks_blueprint.route('/', methods=['GET'])
def get_tasks_by_status() -> Response:
    try:
        status_data = request.args.get('status')
        status = TaskStatus[status_data]
        tasks = tasks_service.get_tasks_by_status(status)
        if tasks:
            return jsonify({'tasks': [task.to_dict() for task in tasks]}), 200
        return jsonify({'message': f'Tasks not found for status: {status.to_str()}'}), 404
    except Exception as e:
        return jsonify({'message': 'Invalid task status'}), 404
