from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import mysql.connector

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    # old SQLite db
    #app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    # new mySQL db
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://admin:gebongkalol@gebongka.c0yrjbkoofev.ap-southeast-1.rds.amazonaws.com/gebongka"
    app.config['SECRET_KEY'] = 'secretkey'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Users

    with app.app_context():
        db.create_all()
        print("created db!")
    # create_database(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app

# def create_database(app):
#     if not path.exists('instance/' + DB_NAME):
#         with app.app_context():
#             db.create_all()
#         print('Created database!')