from flask import Blueprint, jsonify, Response, request
from app.service.configuration import comments_service
from flask_restful import reqparse
from app.db.entity import TaskStatus

comments_blueprint = Blueprint('comments', __name__, url_prefix='/comments/content')


@comments_blueprint.route('/<int:comment_id>', methods=['PATCH', 'PUT'])
def update_comment_content(comment_id: int) -> Response:
    try:
        comment = comments_service.get_by_id(comment_id)
        if not comment:
            return {'message': 'Comment not found'}, 404
        parser = reqparse.RequestParser()
        parser.add_argument('new_content', type=str, required=True, help='New comment content')
        request_data = parser.parse_args()
        new_content = request_data['new_content']
        if comment.has_expected_content(new_content):
            # TODO co zwracac, 304 czy 400
            return {'message': 'Comment already has expected content'}, 400
            # return {'message': 'Comment has already expected content'}, 304
        comments_service.change_comment_content(comment.id, new_content)
        return {'message': 'Comment updated'}, 200
    except Exception as e:
        return {'message': 'Cannot update comment content'}, 500
