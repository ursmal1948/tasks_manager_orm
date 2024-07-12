from flask import Blueprint, jsonify, Response, request
from app.service.configuration import (users_service,
                                       tasks_service,
                                       projects_service,
                                       projects_with_tasks_service,
                                       users_with_projects_service
                                       )
from flask_restful import reqparse

from app.db.entity import TaskStatus

projects_blueprint = Blueprint('projects', __name__, url_prefix='/projects')


@projects_blueprint.route('/', methods=['GET'])
def get_projects():
    user_id = request.args.get('user_id')
    if not users_service.get_by_id(user_id):
        return jsonify({'message': 'User does not exist'}), 401
    user_projects = users_service.get_users_projects(user_id)
    if user_projects:
        return jsonify({'projects': [project.to_dict() for project in user_projects]}), 200
    return jsonify({'projects': []}), 200


#  TODO czy robic tez taki route ze w path bedzie user id, a wbody
#   project name i description.
#       tutaj mam tak ze w pathie mam project_name ,a w json body uerid i descirpiont

# ProjectsWithTasksService
@projects_blueprint.route('/<string:project_name>', methods=['POST'])
def add_project(project_name):
    try:
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, help='User id', required=True)
        parser.add_argument('description', type=str, help='Description of project', required=True)
        request_data = parser.parse_args()
        user_id = int(request_data.get('user_id'))
        description = request_data.get('description')
        if not users_service.get_by_id(user_id):
            return jsonify({'message': 'User does not exist'}), 401
        if projects_service.get_by_name(project_name):
            return jsonify({'message': 'Project already exist'}), 401
        users_with_projects_service.add_project_to_user(
            project_name=project_name,
            project_description=description,
            user_id=user_id
        )
        return jsonify({'message': 'Project added successfully'}), 201

    except Exception as e:
        return jsonify({'message': 'Cannot add project'})


# delete_user_projects
# ustawic relacje, ze jak usuwam projekt to zeby sie usunely tez taski. itd.
@projects_blueprint.route('/', methods=['DELETE'])
def delete_user_projects():
    user_id = request.args.get('user_id')
    user = users_service.get_by_id(user_id)
    if not user:
        return jsonify({'message': 'User does not exist'}), 401
    user_projects = users_service.get_users_projects(user_id)
    if not user_projects:
        # 401 czy 304. TOOD CO ZWRACAC
        return jsonify({'message': 'No projects to delete'}), 401
        # return jsonify({'message': 'No projects to delete'}), 401
    users_with_projects_service.delete_user_projects(user_id=user_id)
    return jsonify({'message': 'Projects deleted successfully'}), 200
