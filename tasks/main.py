from flask import Flask, jsonify
from flask_restful import Api
from flask_migrate import Migrate
from sqlalchemy import inspect

import logging
from app.config import DB_URL, MAIL_SETTINGS
from app.mail.configuration import MailSender
from app.db.configuration import sa
from app.routes.users import users_blueprint
from app.routes.projects import projects_blueprint
from app.routes.tasks import tasks_blueprint
from app.routes.comments import comments_blueprint
from app.routes.task_histories import task_histories_blueprint

from app.routes.resource import (UserNameResource,
                                 UsersListResource,
                                 UserEmailResource,
                                 UserWithProjectResource,
                                 CommentContentResource,
                                 CommentIdResource,
                                 CommentsListResource,
                                 TaskHistoryTaskIdResource
                                 )

logging.basicConfig(level=logging.INFO)


def create_app() -> Flask:
    app = Flask(__name__)

    with (app.app_context()):
        app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

        app.config['SQLALCHEMY_ECHO'] = True

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sa.init_app(app)
        logging.info('------ [ BEFORE CREATE ALL] --------')
        # sa.drop_all()
        # sa.create_all()
        app.config.update(MAIL_SETTINGS)
        MailSender(app, 'ula.malin35@gmail.com')

        # MailSender.send('ula.malin35@gmail.com', f'Task status change', f'<h1>New status of task:</h1>')

        logging.info('------ [ AFTER CREATE ALL] --------')

        # migrate = Migrate(app, sa)

        @app.errorhandler(Exception)
        def handle_error(error: Exception):
            logging.info("---------------- ERROR START----------------")
            logging.error(error)
            logging.info("---------------- ERROR END----------------")

            return {'message': str(error)}, 500

        @app.route('/hello')
        def hello_action():
            return jsonify({
                'author': 'UM',
                'version': 1.0
            })

        app.register_blueprint(tasks_blueprint)
        app.register_blueprint(users_blueprint)
        app.register_blueprint(projects_blueprint)
        app.register_blueprint(comments_blueprint)
        app.register_blueprint(task_histories_blueprint)
        api = Api(app)
        api.add_resource(UserNameResource, '/users/username/<string:name>')
        api.add_resource(UserEmailResource, '/users/email/<string:email>')
        api.add_resource(UsersListResource, '/users')
        api.add_resource(UserWithProjectResource, '/users-with-projects')
        api.add_resource(CommentContentResource, '/comments/<string:content>')
        api.add_resource(CommentIdResource, '/comments/<int:comment_id>')
        api.add_resource(TaskHistoryTaskIdResource, '/task-histories/task-id/<int:task_id>')
        api.add_resource(CommentsListResource, '/comments')

    return app


if __name__ == '__main__':
    create_app()
