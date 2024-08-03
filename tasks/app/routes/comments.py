from flask import Blueprint, jsonify, Response, request
from flask_restful import reqparse
from app.service.configuration import comments_service
from app.db.entity import TaskStatus

comments_blueprint = Blueprint('comments', __name__, url_prefix='/comments')


@comments_blueprint.route('/<int:comment_id>', methods=['PATCH'])
def update_comment_content(comment_id: int) -> Response:
    new_content = request.args.get('new_content')
    if not new_content:
        return jsonify({'message': 'new_content is required'}), 400
    comments_service.change_comment_content(comment_id, new_content)
    return jsonify({'message': 'comment updated'}), 200
