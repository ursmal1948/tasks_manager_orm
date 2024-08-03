from flask import Response, Blueprint, jsonify

from app.service.configuration import task_histories_service

task_histories_blueprint = Blueprint('task-histories', __name__, url_prefix='/task-histories')


@task_histories_blueprint.route('/<int:task_history_id>', methods=['DELETE'])
def delete_task_history(task_history_id: int) -> Response:
    task_histories_service.delete_task_history_by_id(task_history_id)
    return jsonify({'message': 'task history deleted', 'task_id': task_history_id}), 200
