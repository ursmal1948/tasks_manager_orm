from flask import Flask, jsonify, current_app
from flask_restful import Api
from dotenv import load_dotenv
from os import getenv
import logging
from flask import Blueprint, jsonify, Response

from app.db.entity import TaskStatus
from flask_json_schema import JsonSchema
from flask_restful import Api, reqparse
from app.db.configuration import sa
from flask_migrate import Migrate
logging.basicConfig(level=logging.INFO)

from app.routes.projects import projects_blueprint
from app.routes.tasks import tasks_blueprint
from app.routes.users import users_blueprint
from app.routes.comments import comments_blueprint

from app.routes.tasks import tasks_blueprint
from app.db.entity import TaskEntity
from app.routes.resource import (UserNameResource,
                                 UsersListResource,
                                 UserEmailResource,
                                 CommentContentResource,
                                 CommentIdResource,
                                 CommentsListResource,

                                 )
from app.db.repository import user_repository, project_repository
from app.service.configuration import tasks_service, projects_with_tasks_service
from app.config import DB_URL, MAIL_SETTINGS
from app.mail.configuration import MailSender


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
        MailSender(app, 'testowy2.kmprograms@gmail.com')

        # MailSender.send('ula.malin35@gmail.com', f'Task status change', f'<h1>New status of task:</h1>')

        logging.info('------ [ AFTER CREATE ALL] --------')
        migrate = Migrate(app, sa)


        @app.errorhandler(Exception)
        def handle_error(error: Exception):
            logging.info("---------------- ERROR START----------------")
            logging.error(error)
            logging.info("---------------- ERROR END----------------")

            return {'message': str(error)}, 500

        @app.route('/hello')
        def hello_action():
            print('*******************************************')
            # tasks_service.change_status(task_id=2, new_status=TaskStatus.COMPLETED)
            # tasks_service.delete_task(task_id=2)
            # projects_service.change_project_description(project_id=9,description='SOMEDESC')
            # logging.info(tasks_service.get_task_project(task_id=2))
            print('*******************************************')

            # logging.info(projects_service.get_project_tasks(project_id=7))
            # logging.info(users_service.get_users(user_id=1/))
            print('*******************************************')
            # user_repository.save_or_update(UserEntity(
            #     id=1,
            #     name='NEW NAMEEEEEE',
            #     password='OLD PASSWORD',
            #     email='SOME FCKN mail'
            # ))
            logging.info("BLUEPRINTSSSSSSSSSSSSSSSSSSSSSASKDJSASD")

            projects_with_tasks_service.change_task_status(
                task_id=3,
                new_status=TaskStatus.NEW)

            # print(user_repository.find_email_by_id(1))
            # user_id = project_repository.find_user_id_by_project_id(7)
            # logging.info(user_id)
            # project_email = user_repository.find_email_by_id(user_id)
            # logging.info(project_email)

            logging.info("BLUEPRINTSSSSSSSSSSSSSSSSSSSSSASKDJSASD")
            return jsonify({
                'author': 'UM',
                'version': 1.0
            })

        app.register_blueprint(tasks_blueprint)
        app.register_blueprint(users_blueprint)
        app.register_blueprint(projects_blueprint)
        app.register_blueprint(comments_blueprint)
        api = Api(app)
        api.add_resource(UserNameResource, '/users/username/<string:name>')
        api.add_resource(UserEmailResource, '/users/email/<string:email>')
        api.add_resource(CommentContentResource, '/comments/<string:content>')
        api.add_resource(CommentIdResource, '/comments/<int:comment_id>')

        api.add_resource(CommentsListResource, '/comments')
        # api.add_resource(UsersListResource, '/users')

    return app


if __name__ == '__main__':
    create_app()
